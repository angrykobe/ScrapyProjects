# -*- coding: utf-8 -*-

import time
import scrapy
import xlrd
import re
import requests
from urllib.request import quote,unquote
from scrapy.http import Request
from personspider.items import JsonSpiderItem

from lxml import etree, html
from lxml.html import clean
from scrapy.selector import Selector


class personspider(scrapy.Spider):
    name = "person"
    allowed_domains = []
    download_delay = 1
    pattern = re.compile(r'(\s+)',re.I|re.M|re.DOTALL)

    def __init__(self, *args, **kwargs):
        super(personspider, self).__init__(*args, **kwargs)
        self.keywords = self.read_excel();

    def start_requests(self):
        for nid,line in enumerate(self.keywords):
            name = line[0]
            for kid,keyword in enumerate(line):
                yield Request(url= 'https://www.baidu.com/s?ie=utf-8&tn=baidu&wd={}'.format(quote(keyword)),
                                     callback=self.parseurl,
                                     meta={
                                         'name':name,
                                      'keyword': keyword,
                                         'nid':nid,
                                         'kid':kid
                                     },
                                     errback=self.error)


    def parseurl(self,response):
        name = response.meta['name']
        keyword = response.meta['keyword']
        nid = response.meta['nid']
        kid = response.meta['kid']
        requrl = response.url
        containers  = response.xpath('//*[@class="result c-container "]')
        for rid,dic in enumerate(containers):
            item = JsonSpiderItem()
            title = dic.xpath('h3').xpath('string(.)').extract_first()
            baiduurl = dic.xpath('h3/a/@href').extract_first()
            realurl = self.get_real(baiduurl)
            abstract = dic.xpath('string(div[@class="c-abstract"]|div//div[@class="c-abstract"])').extract_first()
            #
            # item['name'] = name
            # item['nid'] = nid
            # item['keyword'] = keyword
            # item['kid'] = kid
            # item['requrl'] = requrl
            # item['rid'] = rid
            # item['title'] = title
            # item['baiduurl'] = baiduurl
            # item['realurl'] = realurl
            # item['abstract']= abstract
            yield Request(url=str(realurl),meta={
                'name': name,
                'nid': nid,
                'keyword': keyword,
                'kid': kid,
                'requrl': requrl,
                'rid': rid,
                'title': title,
                'baiduurl': baiduurl,
                'realurl': realurl,
                'abstract': abstract
            }, callback=self.parse, errback=self.error)
            # yield item

        time.sleep(0.5)

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

        item['name'] = response.meta['name']
        item['nid'] = response.meta['nid']
        item['keyword'] = response.meta['keyword']
        item['kid'] = response.meta['kid']
        item['requrl'] = response.meta['requrl']
        item['rid'] = response.meta['rid']
        item['title'] = response.meta['title']
        item['baiduurl'] = response.meta['baiduurl']
        item['realurl'] = response.meta['realurl']
        item['abstract']= response.meta['abstract']
        item['doc'] = docset
        yield item

    # errors from downloader
    def error(self, failure):
        self.logger.error(repr(failure))

    def get_real(self, o_url):
        '''获取重定向url指向的网址'''
        r = requests.get(o_url, allow_redirects = False)    #禁止自动跳转
        if r.status_code == 302:
            try:
                return r.headers['location']    #返回指向的地址
            except:
                pass
        return o_url    #返回源地址



    def read_excel(self):
        index = [7, 8, 9, 13, 15, 17]
        keywords = []
        excelfile =  xlrd.open_workbook('../mingdan.xls')

        sheet = excelfile.sheet_by_index(0)

        for i in range(1, sheet.nrows):
            name = sheet.cell(i,2).value
            oneline = [name+' '+sheet.cell(i, x).value for x in index]
            oneline.insert(0,name)
            oneline.insert(1,name+' 北京大学')
            oneline.insert(2,name+' 软件与微电子学院')
            oneline.insert(3,name+' 领英')
            keywords.append(oneline);

        return keywords
#