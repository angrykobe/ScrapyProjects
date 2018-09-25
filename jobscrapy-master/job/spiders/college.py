#!/usr/bin/env python
# coding=utf-8

import scrapy
from job.items import CollegeItem

class CollegeSpider(scrapy.spiders.Spider):
    name = 'college'
    allowed_domains = ['sina.com.cn']  # 一定不要加协议

    def start_requests(self):
        request_urls = []
        for i in xrange(1, 240):
            request_urls.append(scrapy.Request(
                'http://kaoshi.edu.sina.com.cn/college/collegelist/view?page={}'.format(i),
                callback=self.parse
            ))
        return request_urls

    def parse(self, response):
        college_list = response.xpath('//div[@class="college_info"]/div/a/h4[@class="college_name"]/text()').extract()
        for i in college_list:
            item = CollegeItem()
            item['name'] = i
            yield item

