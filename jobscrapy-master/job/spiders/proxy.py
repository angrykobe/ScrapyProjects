#!/usr/bin/env python
# coding=utf-8

import scrapy
import json
from job.items import ProxyItem

class ProxySpider(scrapy.spiders.Spider):
    name = 'proxy'
    allowed_domains = ['zhimacangku.com']  # 一定不要加协议

    def __init__(self, api=None, *args, **kwargs):
        super(ProxySpider, self).__init__(*args, **kwargs)
        self._api = api

    def start_requests(self):
        return [scrapy.Request(
                self._api,
                callback=self.parse
            )]


    def parse(self, response):
        r = json.loads(response.body)
        if r['code'] == 0:
            for i in r['data']:
                item = ProxyItem()
                item['ip'] = i['ip']
                item['port'] = i['port']
                yield item
