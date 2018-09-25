#!/usr/bin/env python
# coding=utf-8

import scrapy
from job.items import MajorItem

class MajorSpider(scrapy.spiders.Spider):
    name = 'major'
    allowed_domains = ['sina.com.cn']  # 一定不要加协议

    def start_requests(self):
        request_urls = []
        for i in range(1, 31):
            request_urls.append(scrapy.Request(
                'http://kaoshi.edu.sina.com.cn/college/majorlist?page={}'.format(i),
                callback=self.parse
            ))
        return request_urls

    def parse(self, response):
        name_list = response.xpath('//div[@class="leftWrap clearfix"]/table[@class="tbL2"]/tr/td[1]/a/text()').extract() #20
        code_list = response.xpath('//div[@class="leftWrap clearfix"]/table[@class="tbL2"]/tr/td[2]/text()').extract() #21
        base_list = response.xpath('//div[@class="leftWrap clearfix"]/table[@class="tbL2"]/tr/td[3]/text()').extract() #21
        parent_list = response.xpath('//div[@class="leftWrap clearfix"]/table[@class="tbL2"]/tr/td[4]/text()').extract() #21
        for i in range(len(name_list)):
            item = MajorItem()
            item['major_name'] = name_list[i]
            item['major_code'] = code_list[i + 1]
            item['major_base'] = base_list[i + 1]
            item['major_parent'] = parent_list[i + 1]
            yield item