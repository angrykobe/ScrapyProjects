#!/usr/bin/env python
# coding=utf-8

import scrapy
import urllib
import re
from datetime import datetime, timedelta
from job.items import ZhipinItem, AreaItem
from job.utils import Utils


class ZhipinSpider(scrapy.spiders.Spider):
    name = 'zhipin'
    allowed_domains = ['www.zhipin.com']  # 一定不要加协议

    def parse_homepage(self, response):
        clist = response.xpath('//dl[@class="condition-city show-condition-district"]/dd/a/@href').extract() #/c101010100/
        slist = response.xpath('//div[@class="filter-select-box"]/div[4]/span/div/ul/li/a/@href').extract() #/c100010000/t_801/
        ilist = response.xpath('//div[@class="industry-box"]/ul/li/a/@href').extract() #/i100008-c100010000/

        clist = map(lambda x: x[1:-1], clist)
        slist = map(lambda x: x.split('/')[2], slist)
        ilist = map(lambda x: x[1:-1].split('-')[0], ilist)

        clist.pop(0)
        clist.pop(0)
        slist.pop(0)
        ilist.pop(0)

        for c in clist:
            for s in slist:
                for i in ilist:
                    yield scrapy.Request('https://www.zhipin.com/{0}-{1}/{2}'.format(i, c, s),
                                 callback=self.parse_page)

    def parse_page(self, response):
        if response.status == 403:
            return

        stop = True
        title_list = response.xpath('//div[@class="job-title"]/text()').extract()
        id_list = response.xpath('//div[@class="info-primary"]/h3[@class="name"]/a/@data-jobid').extract()
        salary_list = response.xpath(
            '//div[@class="info-primary"]/h3[@class="name"]/a/span[@class="red"]/text()').extract()
        company_list = response.xpath('//div[@class="company-text"]/h3[@class="name"]/a/text()').extract()
        pub_time_list = response.xpath('//div[@class="info-publis"]/p/text()').extract()
        city_work_degree_list = response.xpath('//div[@class="info-primary"]/p/text()').extract() #3
        address_list = city_work_degree_list[0::3]
        work_list = city_work_degree_list[1::3]
        degree_list = city_work_degree_list[2::3]
        publisher_list = response.xpath('//div[@class="info-publis"]/h3/text()').extract()  # 2
        pname_list = publisher_list[0::2]

        for i in xrange(len(title_list)):
            dt = Utils.get_zhipin_datetime(pub_time_list[i])
            if Utils.valid_date(dt):
                item = ZhipinItem()
                item['city'] = address_list[i].split(' ')[0]
                item['province'] = Utils.get_province_from_city(item['city'])
                item['address'] = address_list[i]
                item['salary_min'] = Utils.sarlary_transform(salary_list[i].split('-')[0])
                item['salary_max'] = Utils.sarlary_transform(salary_list[i].split('-')[1])

                item['uptime'] = str(dt)
                item['pub_time'] = str(dt)
                item['worktime'] = work_list[i]
                item['description'] = ''
                item['degree'] = degree_list[i]
                item['company'] = company_list[i]
                item['type'] = 1 #全职/兼职/实习
                item['sup_text'] = ','.join(response.xpath('//div[@class="job-list"]/ul/li[{}]/div[@class="job-tags"]/span/text()'.format(i + 1)).extract())

                item['position'] = title_list[i]
                item['user_info'] = pname_list[i]
                item['email'] = ''
                item['status'] = 1
                item['source'] = 4  #4表示b
                item['id'] = id_list[i]
                item['refresh_time'] = str(dt)
                stop = False
                yield item

        if stop:
            self.logger.info(
                'the position [%s] of company [%s] which updated at [%s] and refresh at [%s] is invalid!, the page is [%d]',
                item['position'], item['company'], item['uptime'], item['uptime'], self._page)
            return

        next_url = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request('https://www.zhipin.com{}'.format(next_url),
                                 callback=self.parse_page)


    def start_requests(self):
        return [scrapy.Request('https://www.zhipin.com/c100010000',
                               callback=self.parse_homepage)]
