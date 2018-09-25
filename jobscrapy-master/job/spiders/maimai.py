#!/usr/bin/env python
# coding=utf-8

import scrapy
from scrapy.spiders import Spider
from job.items import MaiMaiItem
from job.utils import Utils

import json
import time
from urllib.request import quote, unquote

maimai_key_set = set(['id', 'province','refresh_time','city','address','salary_min','salary_max','uptime','pub_time','worktime','description','degree','company','type','sup_text','position','user_info','email', 'status'])

class MaiMaiSpider(Spider):
    name = "maimai"
    allowed_domains = ["maimai.cn", "open.taou.com"]

    def __init__(self):
        super(Spider, self).__init__()
        self._cookie_index = 0
        self._cookies = []
        self._account = ['+86-18513622612', '+86-18001098529', '+86-15801543268', '+86-13439336309']

    def start_requests(self):
        request_list = []
        for phone in self._account:
            request_list.append(
                scrapy.FormRequest(
                    "https://open.taou.com/maimai/user/v3/login?account={}&u=&access_token=&version=4.18.0&ver_code=android_1235&channel=XiaoMi&vc=Android%207.0%2F24&push_permit=1&net=wifi&open=icon&appid=3&device=Xiaomi%20MIX&imei=e6a3cb8d41e5733e&density=2.75".format(phone),
                    formdata={
                        'info_type': '2',
                        'password': 'Zf621001',
                        'stage': 'complete_uinfo',
                        'imei': 'e6a3cb8d41e5733e',
                        'account': phone,
                        'new_fr': '1',
                        'cnt': '3',
                        'dev_type': '3',
                    },
                    callback=self.login_in)
            )
        return request_list


    def login_in(self, response):
        # start_request 模拟登陆，为的是获取cookie
        # print(response)
        body = json.loads(response.body_as_unicode())
        print(body)
        self._cookie_index = self._cookie_index + 1
        self._cookies.append(self._cookie_index)
        yield scrapy.Request('https://maimai.cn/jobs/joblist?' \
                             'fr=tab3&u={0}&access_token={1}&version=4.18.0&ver_code=android_1235' \
                             '&channel=XiaoMi&vc=Android%207.0%2F24&push_permit=1&net=wifi' \
                             '&open=icon&appid=3&device=Xiaomi%20MIX' \
                             '&imei=e6a3cb8d41e5733e&density=2.75&jsononly=1'.format(body['user']['mmid'],
                                                                                     body['token']),
                             meta={'cookiejar': self._cookie_index},
                             cookies={
                                 'u': body['user']['mmid'],
                                 'access_token': body['token'],
                                 'maimai_u': body['user']['mmid'],
                                 'maimai_access_token': body['token'],
                                 'job_invite_msg': ''
                             },
                             callback=self.after_login,
                             )


    @property
    def cookies(self):
        # self.logger.info(self._cookies)
        return self._cookies

    def after_login(self, response):
        if len(self.cookies) < len(self._account):
            return

        for v in Utils.province_city.values():
            for i in Utils.industry_list.keys():
                yield scrapy.Request(
                    'https://maimai.cn/jobs/joblist?page={}&jsononly=1&fr=tab3&professionName={}&majorName={}&province={}&city={}'.format(
                        0, quote(i.encode('utf-8')), quote('全部'), quote(v.encode('utf-8')), quote('全部')),
                    meta = {
                        'province': quote(v.encode('utf-8')),
                        'industry': quote(i.encode('utf-8')),
                        'page': 0
                    },
                    callback=self.parse)


    def valid_date(self, uptime):
        timeArray = time.strptime(uptime, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        if time.time() - int(timestamp) >= 86400:
            return False

        return True


    def parse(self, response):
        js = json.loads(response.body_as_unicode())
        if js['result'] != 'ok' or js['data']['count'] == 0:
            return

        page = response.meta['page']
        province = response.meta['province']
        industry = response.meta['industry']
        data = js['data']['data']

        # print(data)
        for k in data:
            item = MaiMaiItem()
            for key, value in k.items():
                if key in maimai_key_set:
                    item[key] = value
            item['source'] = 2
            item['type'] = Utils.industry_list[unquote(industry).decode('utf-8')]
            if u'天' in item['refresh_time'] and not self.valid_date(item['uptime']):
                self.logger.info('the position [%s] of company [%s] which updated at [%s] and refresh at [%s] is invalid!, the page is [%d]',
                                 item['position'], item['company'], item['uptime'], item['refresh_time'], page)
                return

            if response.status == 403:
                return

            yield item


        yield scrapy.Request(
            'https://maimai.cn/jobs/joblist?page={}&jsononly=1&fr=tab3&professionName={}&majorName={}&province={}&city={}'.format(
                page + 1, industry, quote('全部'), province, quote('全部')),
            meta={
                'province': province,
                'industry': industry,
                'page': page + 1
            },
            callback=self.parse)
