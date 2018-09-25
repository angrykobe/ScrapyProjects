#!/usr/bin/env python
# coding=utf-8

import scrapy
import json
import urllib
from job.items import LagouItem
from job.utils import Utils

class LagouSpider(scrapy.spiders.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']  # 一定不要加协议

    def __init__(self):
        self._cookies = []

    @property
    def cookies(self):
        return self._cookies

    def start_requests(self):
        self._cookies.append(1)
        return [
            scrapy.Request('https://www.lagou.com/jobs/list_',
                            meta={'cookiejar': 1},
                           cookies={
                                'user_trace_token': '20170915114634-783d3bba-99c8-11e7-9191-5254005c3644',
                                'LGUID': '20170915114634-783d4028-99c8-11e7-9191-5254005c3644',
                                '_ga': 'GA1.2.1394324689.1505447193',
                                'index_location_city': '%E5%85%A8%E5%9B%BD',
                            },
                            callback=self.parse_homepage)]



    def parse_homepage(self, response):
        clist = response.xpath('//div[@class="city-wrapper dn"]/a/text()').extract()
        slist= response.xpath('//div[@class="details"]/li[3]/a/text()').extract()
        ilist = response.xpath('//div[@class="has-more hy-area"]/li/a/text()').extract()

        slist.pop(0)
        ilist.pop(0)

        for c in clist:
            for s in slist:
                if '\n' in s:
                    s = s[:s.index('\n')]
                for i in ilist:
                    if '\n' in i:
                        i = i[:i.index('\n')]
                        if i in Utils.industry_list:
                            yield scrapy.FormRequest('https://www.lagou.com/jobs/positionAjax.json?jd={1}&hy={2}&px=new&city={0}&needAddtionalResult=false&isSchoolJob=0'.format(urllib.quote(c.encode('utf-8')), urllib.quote(s.encode('utf-8')), urllib.quote(i.encode('utf-8'))),
                                                     formdata={
                                                         'first': 'false',
                                                         'pn': '1',
                                                         'kd': '',
                                                     },
                                                     meta={
                                                         'pn': 1,
                                                         'jd': urllib.quote(s.encode('utf-8')),
                                                         'hy': urllib.quote(i.encode('utf-8')),
                                                         'city': urllib.quote(c.encode('utf-8'))
                                                     },
                                                     callback=self.parse)


    def parse(self, response):
        if response.status == 403:
            return

        js = json.loads(response.body_as_unicode())
        if not js['success']:
            return

        data = js['content']['positionResult']['result']
        stop = True
        for i in data:
            dt = Utils.get_lagou_datetime(i['formatCreateTime'])
            if Utils.valid_date(dt):
                item = LagouItem()
                item['city'] = i['city']
                item['province'] = Utils.get_province_from_city(i['city'])
                item['address'] = ''
                item['salary_min'] = Utils.sarlary_transform(i['salary'].split('-')[0])
                item['salary_max'] = Utils.sarlary_transform(i['salary'].split('-')[1])
                item['uptime'] = str(dt)
                item['pub_time'] = str(dt)
                item['worktime'] = i['workYear']
                item['description'] = ''
                item['degree'] = i['education']
                item['company'] = i['companyShortName']
                item['type'] = Utils.industry_list[urllib.unquote(response.meta['hy']).decode('utf-8')]
                item['sup_text'] = i['positionAdvantage']
                item['position'] = i['positionName']
                item['user_info'] = i['publisherId']
                item['email'] = ''
                item['status'] = 1
                item['source'] = 3  # 4表示b
                item['id'] = i['positionId']
                stop = False
                yield item

        if stop:
            self.logger.info(
                'the position [%s] of company [%s] which updated at [%s] and refresh at [%s] is invalid!, the page is [%d]',
                item['position'], item['company'], item['uptime'], item['uptime'], self._page)
            return

        if response.meta['pn'] < 30:
            yield scrapy.FormRequest(
                'https://www.lagou.com/jobs/positionAjax.json?jd={1}&hy={2}&px=new&city={0}&needAddtionalResult=false&isSchoolJob=0'.format(response.meta['city'], response.meta['jd'], response.meta['hy']),
                formdata={
                    'first': 'false',
                    'pn': str(response.meta['pn'] + 1),
                    'kd': '',
                },
                meta={
                    'pn': response.meta['pn'] + 1,
                    'jd': response.meta['jd'],
                    'hy': response.meta['hy'],
                    'city': response.meta['city']
                },
                callback=self.parse)

