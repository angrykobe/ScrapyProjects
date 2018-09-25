# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    uptime = scrapy.Field()
    pub_time = scrapy.Field()
    worktime = scrapy.Field()
    description = scrapy.Field()
    degree = scrapy.Field()
    company = scrapy.Field()
    type = scrapy.Field()
    sup_text = scrapy.Field()
    position = scrapy.Field()
    user_info = scrapy.Field()
    email = scrapy.Field()
    status = scrapy.Field()
    id = scrapy.Field()
    source = scrapy.Field()
    refresh_time = scrapy.Field()


class MaiMaiItem(JobItem):
    pass


class LagouItem(JobItem):
    pass


class ZhipinItem(JobItem):
    pass


class CollegeItem(scrapy.Item):
    name = scrapy.Field()


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()


class MajorItem(scrapy.Item):
    major_base = scrapy.Field()
    major_parent = scrapy.Field()
    major_code = scrapy.Field()
    major_name = scrapy.Field()


class AreaItem(scrapy.Item):
    city = scrapy.Field()
    district = scrapy.Field()
    area = scrapy.Field()


class JobUiItem(scrapy.Item):
    # 公司名
    name = scrapy.Field()
    # 浏览量
    views = scrapy.Field()
    # 公司性质
    type = scrapy.Field()
    # 公司规模
    size = scrapy.Field()
    # 行业
    industry = scrapy.Field()
    # 公司简称
    abbreviation = scrapy.Field()
    # 公司信息
    info = scrapy.Field()
    # 好评度
    praise = scrapy.Field()
    # 薪资区间
    salary_range = scrapy.Field()
    # 公司产品
    products = scrapy.Field()
    # 融资情况
    financing_situation = scrapy.Field()
    # 公司排名
    rank = scrapy.Field()
    # 公司地址
    address = scrapy.Field()
    # 公司网站
    website = scrapy.Field()
    # 公司logo
    logo = scrapy.Field()

