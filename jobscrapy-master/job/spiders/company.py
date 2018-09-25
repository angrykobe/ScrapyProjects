#!/usr/bin/env python
# coding=utf-8

import scrapy

# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.spiders import Spider
# from scrapy.contrib.linkextractors import LinkExtractor
from job.items import JobUiItem


class CompanySpider(scrapy.spiders.Spider):
    name = 'company'
    allowed_domains = ['jobui.com']

    def start_requests(self):
        return [
            scrapy.Request('http://www.jobui.com/changecity',  # 热点城市
                           callback=self.parse_city)
        ]

    def parse_city(self, response):
        hlist = response.xpath('//div[@class="rapid cfix box"]/p[@class="hotCity"]/a/@href').extract()  # 热门城市
        for h in hlist:
            city = h.split('=')[1]
            yield scrapy.Request('http://www.jobui.com/cmp?area={}'.format(city),
                                 meta={'city': city},
                                 callback=self.parse)

    def parse(self, response):
        tlist = response.xpath('//dl[@class="screen jk-box jk-matter"]/dd[2]/a/@href').extract()  # 性质
        dlist = response.xpath('//dl[@class="screen jk-box jk-matter"]/dd[3]/a/@href').extract()  # 地区
        slist = response.xpath('//dl[@class="screen jk-box jk-matter"]/dd[4]/a/@href').extract()  # 规模
        ilist = response.xpath('//dl[@class="screen jk-box jk-matter"]/dd[1]/a/@href').extract()  # 行业

        ilist.pop(0)
        tlist.pop(0)
        dlist.pop(0)
        slist.pop(0)

        for i in ilist:
            for t in tlist:
                for d in dlist:
                    for s in slist:
                        yield scrapy.Request(
                            'http://www.jobui.com/cmp?area={4}&{0}&{1}&{2}&{3}&sortField=sortView'.format(
                                i.split('&')[1],
                                t.split('&')[1],
                                d.split('&')[1],
                                s.split('&')[1],
                                response.meta['city']),
                            callback=self.parse_list)

    def parse_list(self, response):
        next = response.xpath('//a[@class="pg-updown"]/@href').extract()
        next_text = response.xpath('//a[@class="pg-updown"]/text()').extract()
        for i in xrange(len(next_text)):
            if next_text[i] == u'下一页':
                yield scrapy.Request('http://www.jobui.com{}'.format(next[i]),
                                     callback=self.parse_list)

        comp_list = response.xpath('//div[@class="atn-content"]/h2/span[@class="fl"]/a/@href').extract()
        for i in comp_list:
            yield scrapy.Request('http://www.jobui.com{}'.format(i),
                                 callback=self.parse_item)

    def parse_item(self, response):
        # 实例化item对象
        item = JobUiItem()

        # 使用xpath提取数据

        # 公司名称
        item['name'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        # 浏览量
        item['views'] = response.xpath('//div[@class="grade cfix sbox"]/div[1]/text()').extract_first().split(u'人')[
            0].strip()

        """
            有些公司的详情页面没有图片
            所以页面的结构有些不同
        """
        item['type'] = ''
        item['size'] = ''

        type_size = response.xpath('//div[@class="cfix fs16"]/dl/dd[1]/text()').extract_first()
        if '/' in type_size:
            item['type'] = type_size.split('/')[0]
            item['size'] = type_size.split('/')[1]
        else:
            type_size = response.xpath('//*[@id="cmp-intro"]/div/div/dl/dd[1]/text()').extract_first()
            if '/' in type_size:
                item['type'] = type_size.split('/')[0]
                item['size'] = type_size.split('/')[1]

        # 行业
        item['industry'] = response.xpath('//dd[@class="comInd"]/a[1]/text()').extract_first()
        # 公司简称
        item['abbreviation'] = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[3]/text()').extract_first()
        # 公司信息
        item['info'] = ''.join(response.xpath('//*[@id="textShowMore"]/text()').extract())
        # 好评度
        item['praise'] = response.xpath('//div[@class="swf-contA"]/div/h3/text()').extract_first()
        # 薪资区间
        item['salary_range'] = response.xpath('//div[@class="swf-contB"]/div/h3/text()').extract_first()
        # 公司产品
        item['products'] = response.xpath('//div[@class="mb5"]/a/text()').extract()

        # 融资情况
        data_list = []
        node_list = response.xpath('//div[5]/ul/li')
        for node in node_list:
            temp = {}
            # 融资日期
            temp['date'] = node.xpath('./span[1]/text()').extract_first()
            # 融资状态
            temp['status'] = node.xpath('./h3/text()').extract_first()
            # 融资金额
            temp['sum'] = node.xpath('./span[2]/text()').extract_first()
            # 投资方
            temp['investors'] = node.xpath('./span[3]/text()').extract_first()

            data_list.append(temp)

        item['financing_situation'] = data_list

        # 公司排名
        data_list = []
        node_list = response.xpath('//div[@class="fs18 honor-box"]/div')
        for node in node_list:
            temp = {}

            key = node.xpath('./a/text()').extract_first()
            temp[key] = int(node.xpath('./span[2]/text()').extract_first())
            data_list.append(temp)

        item['rank'] = data_list

        # 公司地址
        item['address'] = response.xpath('//dl[@class="dlli fs16"]/dd[1]/text()').extract_first()
        # 公司网址
        item['website'] = response.xpath('//dl[@class="dlli fs16"]/dd[2]/a/text()').extract_first()
        # 公司logo
        item['logo'] = response.xpath('//div[@class="company-logo"]/a/img/@src').extract()

        yield item
