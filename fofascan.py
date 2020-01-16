#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 2.7
# mysql 新建数据库fofa，字符集 utf8mb4  表 fofa_spider  / 导入 fofa.sql

import sys
import requests
import time
import json
import base64
import traceback
import logging
from DBUtils.PooledDB import PooledDB
import pymysql

pymysql.install_as_MySQLdb()

# 禁用安全请求警告 python 3 (下面2行)
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 禁用安全请求警告  python2  (下面2行)

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 配置日志打印信息
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] :%(levelname)s: %(message)s')

# python2
reload(sys)
sys.setdefaultencoding('utf-8')
# python3   Python3字符串默认编码unicode, 所以sys.setdefaultencoding也不存在了


host = 'localhost'
# 数据库连接用户名
user = 'root'
# 数据库连接密码
pwd = 'root'
# 数据库名称
db_name = 'fofa'
# 端口号，默认不需要更改
port = 3306
# 编码，默认不需要更改
charset = 'utf8'
# FOFA 用户名
fofa_name = ''
# FOFA 用户key
fofa_key = ''
# FOFA 每页数量,默认为1万可自行修改
page_size = 100 # 10000
# 起始页码，默认不需要更改
page_start = 1
# 终止页码,会自动计算计算结果为最大页数，默认不需要更改
page_end = 1
# 爬虫字段 host,ip,端口,协议,国家,省份,城市，默认不需要更改（建议不要修改）
fields = ['host', 'ip', 'port', 'protocol', 'country', 'region', 'city']

# port,protocol,country,region,city,host
pool = PooledDB(pymysql, 20, host=host, user=user, passwd=pwd, db=db_name, port=port, charset=charset)
connection = pool.connection()
cursor = connection.cursor()

session = requests.session()
# 请求头
headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

'''
请求中心，控制程序所有HTTP请求，如果请求发生错误进行尝试再次连接
@param url 请求连接
@return 请求响应结果
'''


def fofa_requests(url):
    rs_content = ''
    error_content = ''
    while True:
        try:
            logging.info(url)
            rs = session.get(url, verify=False, headers=headers)
            rs_text = rs.text
            error_content = rs_text
            results = json.loads(rs_text)
            total_size = results['size']
            error = results
            if results['error'] and 'None' not in results['error']:
                info = u'fofa 错误:' + results['error'] + u' 休眠30s'
                logging.error(info)
                time.sleep(30)
            else:
                rs_content = results
                break
        except Exception as e:
            logging.error(error_content)
            logging.error(u'fofa 错误:' + str(e.message) + u' 休眠30s')
            traceback.print_exc()
            time.sleep(30)
    return rs_content


'''
批量数据存入数据库
@param results
@param page_no 当前页数
@param page_total 总页数
'''


def batch_insert_db(results, page_no, page_total, fofa_sql):
    try:
        Z = []
        for result in results:
            a = (str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]),
                 str(result[6]), pymysql.escape_string(fofa_sql))
            Z.append(a)
        sql = "INSERT IGNORE INTO fofa_spider(id,host,ip,port,protocol,country_name,region_name,city_name,fofa_sql,create_date,update_date) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
        cursor.executemany(sql, Z)
        connection.commit()
        logging.info(u'存入数据库ok,总数量为:' + str(len(Z)) + u', page--> ' + str(page_no) + '/' + str(page_total))
    except Exception as e:
        logging.error(u"存入数据库错误,错误信息:" + e.message)
        traceback.print_exc()


'''
fofa 爬虫主函数
@param fofa_sql fofa查询语句
'''


def main(fofa_sql):
    base64_str = base64.b64encode(fofa_sql)
    fields_str = ','.join(fields)
    api_url = 'http://fofa.so/api/v1/search/all?email=' + fofa_name + '&key=' + fofa_key + '&fields=' + fields_str + '&size=' + str(
        page_size) + '&page=' + str(page_start) + '&qbase64=' + base64_str
    rs = fofa_requests(api_url)
    total_size = rs['size']
    # 计算页数
    page_end = total_size / page_size + 1 if total_size % page_size != 0 else total_size / page_size
    # 存入u 数据库
    batch_insert_db(rs['results'], page_start, page_end, fofa_sql)
    for page_no in range(2, page_end + 1):
        api_url = 'http://fofa.so/api/v1/search/all?email=' + fofa_name + '&key=' + fofa_key + '&fields=' + fields_str + '&size=' + str(
            page_size) + '&page=' + str(page_no) + '&qbase64=' + base64_str
        rs = fofa_requests(api_url)
        batch_insert_db(rs['results'], page_no, page_end, fofa_sql)


if __name__ == '__main__':
    fofa_sql = 'app="Seeyon-Server" || app="用友-致远OA"'
    main(fofa_sql)
