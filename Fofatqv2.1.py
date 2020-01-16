#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__:leezp
# __date__:2019-08-02
# Local:  Win7 (python3)
# Fofatq v2.1

import requests
from urllib import parse
import urllib
import base64
from bs4 import BeautifulSoup
import time
import random
import datetime

User_Agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)'
]

PROXIES = ['http://117.85.48.16:9999',
           'http://182.34.34.213:9999',
           'http://175.42.122.3:9999']


class FofaSpider:
    def __init__(self, query_str, Cookie, Referer, X_CSRF_Token, If_None_Match):
        self.query_str_urlencode = urllib.parse.quote(query_str)
        query_str_qbase64 = str(base64.b64encode(query_str.encode('utf-8')), 'utf-8')
        self.query_str_qbase64_urlencode = urllib.parse.quote(query_str_qbase64)
        self.headers = {
            'Accept': 'application/ecmascript, application/x-ecmascript, */*,q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'fofa.so',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': '%s' % (random.choice(User_Agents)),
            'Cookie': '%s' % (Cookie)
        }

    def file_put(self, str):
        with open("ip.txt", "a", encoding='utf-8') as f:
            f.write(str)

    def spider_ip(self, url, i):
        try:
            # if (i % 15 == 0):  # 每15页休眠20秒
            #    time.sleep(20)
            response = requests.get(url=url, proxies=random.choice(PROXIES), headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
            all_t = soup.find_all("div", class_="list_mod_t")
            all_c = soup.find_all("div", class_="list_mod_c")

            if len(all_t) != 0:  # 判断session 是否返回正确页面/Status Code: 429
                count = 0
                for k in all_t:
                    num = k.find_all('a')
                    if ("http" in num[0].get('href')) & ("https" not in num[0].get('href')):
                        ip = num[0]['href']
                        self.file_put(ip)  # 写ip
                        text = all_c[count].find_all("ul", class_="list_sx1")
                        text = text[0].find_all("li")[0]
                        title = text.text.strip()  # 写title 并去除空格
                        self.file_put(",            " + title + "\n")
                    count += 1
            else:
                print(str(i) + " none")  # 爬16页 左右页面显示 Retry later；状态码 Status Code: 429 Too Many Requests
                time.sleep(20)  # 等待20秒
                # 重新爬取丢失这一页
                try:
                    response = requests.get(url=url, proxies=random.choice(PROXIES), headers=self.headers, timeout=5)
                    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
                    all_t = soup.find_all("div", class_="list_mod_t")
                    all_c = soup.find_all("div", class_="list_mod_c")
                    if len(all_t) != 0:  # 判断session 是否失效
                        count = 0
                        for k in all_t:
                            num = k.find_all('a')
                            if ("http" in num[0].get('href')) & ("https" not in num[0].get('href')):
                                ip = num[0]['href']
                                self.file_put(ip)  # 写 ip
                                text = all_c[count].find_all("ul", class_="list_sx1")
                                text = text[0].find_all("li")[0]
                                title = text.text.strip()  # 打印title 并去除空格
                                self.file_put(",            " + title + "\n")
                            count += 1
                    print('第' + str(i) + '页第二次爬取成功')
                except:  # 这个except没有走，走的外层except,暂未解决
                    # print('第二次重连失败，第' + i + '页')
                    # time.sleep(20)
                    pass
        except requests.exceptions.ReadTimeout as E:
            print(str(i), end=' ')  # end=' '不换行输出
            print(E)
            # 将异常的页码保存到ipexcept.txt，便于单独跑，不遗漏数据
            with open("ipexcept.txt", "a", encoding='utf-8') as f:
                f.write(str(i) + "\n")
            pass

    def base(self, start, page):
        for i in range(start, page):
            query_url = "https://fofa.so/result?page=" + str(
                i) + "&qbase64=" + fofaSpider.query_str_qbase64_urlencode  # "&q=" + fofaSpider.query_str_urlencode +
            print("第" + str(i) + "页 " + query_url)
            fofaSpider.spider_ip(query_url, i)

    def runipexcept(self):
        f = open("ipexcept.txt", "r", encoding='utf-8')
        for line in f:
            query_url = "https://fofa.so/result?page=" + str(
                line.strip()) + "&qbase64=" + fofaSpider.query_str_qbase64_urlencode
            print("第" + str(line.strip()) + "页 " + query_url)
            fofaSpider.spider_ip(query_url, line.strip())


if __name__ == "__main__":
    # query_str 查询字符串
    query_str = '"memcached"'
    Cookie = '_fofapro_ars_session=XXX'
    X_CSRF_Token = ''
    Referer = ''
    If_None_Match = ''

    fofaSpider = FofaSpider(query_str, Cookie, Referer, X_CSRF_Token, If_None_Match)
    # 要爬取得页数，page=n+1,page = 2 则只爬取第一页

    starttime = datetime.datetime.now()
    fofaSpider.base(1, 21)
    # fofaSpider.runipexcept()  # 跑完 base()这个方法，跑 runipexcept()这个方法，把剩余IP自动跑一边
    endtime = datetime.datetime.now()
    print('程序结束', end=' ')
    print(datetime.datetime.now())
    print('耗时', end=' ')
    print(endtime - starttime, end=' ')
    print('秒')
