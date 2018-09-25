#!/usr/bin/env python
# coding=utf-8

import scrapy
import urllib
from job.items import AreaItem


class LagouSpider(scrapy.spiders.Spider):
    name = 'area'
    allowed_domains = ['lagou.com']  # 一定不要加协议

    def __init__(self):
        self._cookies = []

    @property
    def cookies(self):
        return self._cookies

    def start_requests(self):
        self._cookies.append(1)
        return [
            scrapy.Request('https://www.lagou.com/jobs/allCity.html?px=new&city=%E5%85%A8%E5%9B%BD&positionNum=500+&companyNum=0&isCompanySelected=false&labelWords=',
                            meta={'cookiejar': 1},
                            cookies={
                                'user_trace_token': '20170915114634-783d3bba-99c8-11e7-9191-5254005c3644',
                                'LGUID': '20170915114634-783d4028-99c8-11e7-9191-5254005c3644',
                                '_ga': 'GA1.2.1394324689.1505447193',
                                'index_location_city': '%E5%85%A8%E5%9B%BD',
                            },
                            callback=self.parse)]

    def parse(self, response):
        city_list = response.xpath('//ul[@class="city_list"]/li/a/text()').extract()
        city_url_list = response.xpath('//ul[@class="city_list"]/li/a/@href').extract()

        for i in xrange(len(city_url_list)):
            city_url_list[i] = city_url_list[i].strip()
            if not city_url_list[i].endswith('-zhaopin/'):
                city_url_list[i] = city_url_list[i][0:-1] + '-zhaopin/'

            yield scrapy.Request(city_url_list[i],
                                 meta={'city': city_list[i]},
                                 callback=self.parse_district)


    def parse_district(self, response):
        district_list = response.xpath('//div[@class="detail-items districts-wrapper"]/a/text()').extract()
        if not district_list:
            district_list = response.xpath('//div[@class="contents"][1]/a/text()').extract()

        if district_list:
            district_list.pop(0) #去掉不限

        for i in district_list:
            yield scrapy.Request('https://www.lagou.com/jobs/list_?px=new&city={0}&district={1}#filterBox'.format(urllib.quote(response.meta['city'].encode('utf-8')), urllib.quote(i.encode('utf-8'))),
                                 meta={
                                     'city': response.meta['city'],
                                     'district': i,
                                 },
                                 callback=self.parse_area)


    def parse_area(self, response):
        area_list = response.xpath('//div[@class="detail-items"]/a/text()').extract()

        for i in area_list:
            item = AreaItem()
            item['city'] = response.meta['city']
            item['district'] = response.meta['district']
            item['area'] = i
            yield item

