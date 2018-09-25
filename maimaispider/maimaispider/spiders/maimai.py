#!/usr/bin/env python
# coding=utf-8

import scrapy
from scrapy.spiders import Spider
# from job.items import MaiMaiItem
# from job.utils import Utils

import json
import time

from urllib.request import quote, unquote

maimai_key_set = set(['id', 'province','refresh_time','city','address','salary_min','salary_max','uptime','pub_time','worktime','description','degree','company','type','sup_text','position','user_info','email', 'status'])

import scrapy
from scrapy.http import Request,FormRequest

class MaiMaiSpider(scrapy.Spider):                                       #定义爬虫类，必须继承scrapy.Spider
    name = 'maimai'                                                     #设置爬虫名称
    allowed_domains = ["maimai.cn","open.taou.com"]                  #爬取域名
    # start_urls = ['http://edu.iqianyue.com/index_user_login.html']     #爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息
    jobquene = Queue()

    idSet = set()
    mmidQ = []

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}  #设置浏览器用户代理

    def start_requests(self):       #用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request('https://acc.maimai.cn/login',
                        headers=self.header,
                        meta={'cookiejar':1},
                        callback=self.parse)]

    def parse(self, response):     #parse回调函数

        data = {                    #设置用户登录信息，对应抓包得到字段
            'm':'13269352113',
            'p':'lincc4769456',
            'to':'',
            'pa':'+86'
        }

        # 响应Cookie
        print(response.headers)
        Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print(Cookie1)

        print('登录中')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        return [FormRequest.from_response(response,
                                          url='https://acc.maimai.cn/login',   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          headers=self.header,
                                          formdata=data,
                                          callback=self.next,
                                          )]
    def next(self,response):
        a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息

        print(a)

        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('https://maimai.cn/contact/detail/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1Ijo0ODk2OSwibGV2ZWwiOjAsInQiOiJjdHQifQ.2JFlLq3cS9_1_blcF17EcFnNZr9dir6B1w4yd7IgtK4?from=webview%23%2Ffeed_list', meta={'cookiejar':True}, callback=self.next2)
    def next2(self,response):

        # 请求Cookie
        Cookie2 = response.request.headers.getlist('Cookie')
        print(Cookie2)

        body = response.body  # 获取网页内容字节类型
        unicode_body = response.body_as_unicode()  # 获取网站内容字符串类型
        print('feedlist ', unicode_body)


    def getUrl(self, response):
        js = json.loads(response.body, encoding='utf-8')
        data = js['data']['card']
        for item in data :
            if item['card']['id'] not in self.idDict:
                self.idSet.add(item['card']['id'])
                self.mmidQ.append(item['card']['mmid'])

    def detllUrl(self, encode_mmid):
        return 'https://maimai.cn/contact/detail/'+ encode_mmid + '?from=webview%23%2Ffeed_list'

    def itrtUrl(self, encode_mmid):
        return  'https://maimai.cn/contact/interest_contact/'+ encode_mmid + '?jsononly=1'

