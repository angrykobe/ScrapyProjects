# -*- coding: utf-8 -*-

import time
import scrapy
import xlrd
import re
import json
import requests
from urllib.request import quote,unquote
from scrapy.http import Request
from personspider.items import JsonSpiderItem

from lxml import etree, html
from lxml.html import clean
from scrapy.selector import Selector


class person2spider(scrapy.Spider):
    name = "person2"
    allowed_domains = []
    download_delay = 1
    pattern = re.compile(r'(\s+)',re.I|re.M|re.DOTALL)

    def __init__(self, *args, **kwargs):
        super(person2spider, self).__init__(*args, **kwargs)
        self.person = self.jsonload();

    def start_requests(self):
        for one in self.person:
            yield Request(url=one['realurl'],
                          callback=self.parse,
                          meta={
                              'one': one
                          },
                          errback=self.error)

    def parse(self, response):
        title = response.xpath('//head/title/text()').extract_first()
        title = self.pattern.sub(" ",title).strip() if title != None else ""
        keywords = response.xpath('//head/meta[@name="keywords"]/@content').extract_first()
        keywords = self.pattern.sub(" ",keywords).strip() if keywords != None else ""
        description = response.xpath('//head/meta[@name="description"]/@content').extract_first()
        description = self.pattern.sub(" ",description).strip() if description != None else ""

        cleaner = clean.Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=False)
        html1 = cleaner.clean_html(response.text)
        # print(response.url)
        doc = html.fromstring(html1)
        content =self.pattern.sub(" ",doc.xpath('//body')[0].text_content())
        #
        docset = dict()
        docset['title'] = title
        docset['keyword'] = keywords
        docset['description'] = description
        docset['content'] = content
        item = JsonSpiderItem()

        one = response.meta['one']
        item['name'] = one['name']
        item['nid'] = one['nid']
        item['keyword'] = one['keyword']
        item['kid'] = one['kid']
        item['requrl'] = one['requrl']
        item['rid'] = one['rid']
        item['title'] = one['title']
        item['baiduurl'] = one['baiduurl']
        item['realurl'] = one['realurl']
        item['abstract']= one['abstract']
        item['doc'] = docset
        yield item

    # errors from downloader
    def error(self, failure):
        self.logger.error(repr(failure))

    def jsonload(self):
        person = []
        with open('result_nodoc.json', 'r', encoding='utf-8') as f:
            for line in f:
                person.append(dict(json.loads(line)))
        return person
#