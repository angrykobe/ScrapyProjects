# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GaoxiaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sch_area = scrapy.Field()
    sch_name = scrapy.Field()
    sch_url = scrapy.Field()
    sch_abbr = scrapy.Field()
    sch_pfix = scrapy.Field()
    # pass
