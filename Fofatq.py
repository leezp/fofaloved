#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__:leezp
# __date__:2019-07-04
# Local:  Win7 (python3)
# fofa Power raising

import requests
from urllib import parse
import urllib
import base64
from bs4 import BeautifulSoup

class FofaSpider:
    def __init__(self, query_str, Cookie, Referer, X_CSRF_Token, If_None_Match):
        self.query_str_urlencode = urllib.parse.quote(query_str)
        query_str_qbase64 = str(base64.b64encode(query_str.encode('utf-8')), 'utf-8')
        self.query_str_qbase64_urlencode = urllib.parse.quote(query_str_qbase64)
        self.headers = {
            # 'Accept':'*/*',  # OK
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
       
        response = requests.get(url=url, headers=self.headers) 
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

        all_t = soup.find_all("div", class_="list_mod_t")
        all_c = soup.find_all("div", class_="list_mod_c")

        count = 0
        for k in all_t:
            num = k.find_all('a')
            # 根据需要过滤https,只留下http
            if ("http" in num[0].get('href')) & ("https" not in num[0].get('href')):
                ip = num[0]['href']
                self.file_put(ip)
                text = all_c[count].find_all("ul", class_="list_sx1")
                text = text[0].find_all("li")[0]
                title = text.text.strip()  # 打印title 并去除空格
                self.file_put(",            " + title + "\n")
            count += 1

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
