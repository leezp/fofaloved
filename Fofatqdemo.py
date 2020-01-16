#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__:leezp
# __date__:2019-07-04
# Local:  Win7 (python3)
# pip install lxml
# beautifulsoup教程 # https://www.jianshu.com/p/55fc16eebea4
# fofa 提权高级会员

import requests
from urllib import parse
import urllib
import base64
from bs4 import BeautifulSoup

'''
python3 base64加密两种写法
第一种写法:
byte_s = base64.b64encode(query_str.encode('utf-8'))
query_str_qbase64 =str(byte_s,'utf-8')
第二种写法：
byte_s=base64.b64encode(query_str.encode('utf-8'))
#b = str(byte_s)
#print(b[2:-1])
'''


class FofaSpider:
    def __init__(self, query_str, Cookie, Referer, X_CSRF_Token, If_None_Match):
        self.query_str_urlencode = urllib.parse.quote(query_str)
        query_str_qbase64 = str(base64.b64encode(query_str.encode('utf-8')), 'utf-8')
        self.query_str_qbase64_urlencode = urllib.parse.quote(query_str_qbase64)
        self.headers = {
            # 'Accept':'*/*',  # OK
            # "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",# 直接复制网页的，导致网页格式出错
            'Accept': 'application/ecmascript, application/x-ecmascript, */*,q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'fofa.so',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'If-None-Match': '%s' % (If_None_Match),
            'Referer': '%s' % (Referer),
            'Cookie': '%s' % (Cookie),
            'X-CSRF-Token': '%s' % (X_CSRF_Token)
        }

    def file_put(self, str):
        with open("ip.txt", "a", encoding='utf-8') as f:
            f.write(str)

    def spider_ip(self, url):
        '''
        这里出了一个问题，思维阻塞了一天才发现原因。写了一个test脚本测试
        response = requests.get(url)
        soup=BeautifulSoup(response.text,'lxml')
        all_k = soup.find_all('div',class_="list_mod_t")
        print (all_k)
        发现不加 headers是可以打印出结果的，将headers中所有元素注释，发现可以跑出结果，
        将headers中json字段逐条注释，发现 accept 字段出了问题，去掉accept字段可以打印，问题已定位
        将accept 字段改为：'Accept':'*/*', 可以访问，将从目标页面复制的 accept 的value 值逐个注释，最终定位
        出错的 value值：text/javascript, application/javascript, 去掉这两个value 可以打印，
        经过调试，原来 'Accept':'*/*' requests.get 打印出 html 格式 数据，加上出错的value值将html数据转义，" 变成了 \"，
        还有引起了 <a 标签不闭合等问题，比如 for link in soup.find_all('a',href = re.compile('http:')):  beautifulsoup 爬a 标签会找不到闭合 </a>标签
        
        结论 requests.get 打印出的网页 格式与 accept字段密切相关，默认打印html格式页面
        
        '''
        response = requests.get(url=url, headers=self.headers)  
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

        all_t = soup.find_all("div", class_="list_mod_t")
        all_c = soup.find_all("div", class_="list_mod_c")
        # 原理很简单，list_mod_t和list_mod_c都是10组标签，遍历，设置一个计数器，发现目标数据 记录list[count]
        # print(all_k)
        count = 0
        for k in all_t:
            num = k.find_all('a')
            if ("http" in num[0].get('href')) & ("https" not in num[0].get('href')):
                ip = num[0]['href']
                self.file_put(ip)
                text = all_c[count].find_all("ul", class_="list_sx1")
                text = text[0].find_all("li")[0]
                title = text.text.strip()  # 打印title 并去除空格
                self.file_put(",            " + title + "\n")
            count += 1

        # k.parent 定位会出错，用 num[0].parent
        # a标签父节点的下一个兄弟节点
        # print (num[0].parent.next_siblings) #list_iterator类型
        # 遍历
        # 通过 for迭代已知道 list_mod_c 在第二个元素，所以做个判断

        '''  q= 0
            for sibling in num[0].parent.next_siblings:
                if (q==1):
                    print(sibling)
                    soup2=BeautifulSoup(sibling.text,'lxml')
                    all_c=soup2.findall("div", class_="list_mod_c")
                    print (all_c)
                    break
                q+=1'''

        '''
        for link in soup.find_all('a'):
            if ("http:" in link.get('href')):
                ip = link.get('href')  # 等价于 ip=link["href"]  # '\"http://14.155.220.91:8443\"'
                # result = re.findall(r"\d+\.\d+\.\d+.\d+(:\d\d\d\d|:\d\d\d|:\d\d|)", ip, re.I)
                self.file_put(ip + "\n")
                '''


if __name__ == "__main__":
    # query_str 查询字符串
    query_str = 'app="用友-致远OA"'
    If_None_Match = 'W/"004099f9f8098bec5edc68de7d218055"'
    X_CSRF_Token = ''
    Cookie = ''
    Referer = ''
    # referer_url加密：base64之后进行urlencode 再结合 result一起urlencode

    fofaSpider = FofaSpider(query_str, Cookie, Referer, X_CSRF_Token, If_None_Match)
    # 要爬取得页数，page=n+1,page = 2 则只爬取第一页
    page = 16
    for i in range(1, page):
        query_url = "https://fofa.so/result?page=" + str(
            i) + "&q=" + fofaSpider.query_str_urlencode + "&qbase64=" + fofaSpider.query_str_qbase64_urlencode
        fofaSpider.spider_ip(query_url)
