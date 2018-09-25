# -*- coding: utf-8 -*-


import scrapy
import re
from scrapy.http import Request,FormRequest
from gaoxiaospider.items import GaoxiaospiderItem


class gaoxiaospider(scrapy.Spider):
    name = "gaoxiao"
    allowed_domains = ["u.feelingmsg.com"]
    download_delay = 1

    path = 'http://u.feelingmsg.com/u/'

    def start_requests(self):
        # url = ["http://u.feelingmsg.com/u/"]
        return [Request(url='http://u.feelingmsg.com/u/',
                        # headers=self.header,
                        # meta={'cookiejar':1},
                        callback=self.parseprovince)]

    def parseprovince(self, response):

        sch_urls = [x for x in response.xpath('//a/@href').extract() if x.endswith('.php')]
        sch_names = response.xpath('//a/span[@class="style12he"]/text()').extract()
        print(sch_urls)
        print(sch_names)
        names_urls = zip(sch_names,sch_urls)
        for item in names_urls:
            print(item)


            name = item[0]
            url = item[1]
            print(name, '', url)
            if url.startswith('helong'): url = 'heilongjiang.php'
            in_url = "{}{}".format(self.path, url)
            print(in_url)
            yield Request(url=in_url,meta={
                'sch_area':name
            }, callback=self.parse)
        # print(names_urls)
        # print(response.body_as_unicode())
        # kk = 'ddddddddddddd<a target=blank href=guangdong.php><span class=style12he>广东</span></a>dddddddddd'
        # matchs = re.findall(r"<a target=blank href=\w+\.php><span class=style12he>.+</span></a>",response.body_as_unicode(),re.M)
        # # re.
        # print(matchs[0])
        # sub  = re.sub(r'(<a target=blank href=)|(><span class=style12he>)|(</span></a></td><td align=center>)|(</span></a></td></tr><tr><td align=center>)'," ", matchs[0])
        # subs = sub.strip().split()

        # sch_name = re.sub(r'\w+\.php',"", matchs[0])
        # print(subs)
        # print(sch_name)

    def parse(self, response):
        sch_urls = response.xpath('//span[contains(@class,"STYLE")]/a/@href').extract()[2:]
        sch_names = response.xpath('//span[contains(@class,"STYLE")]/a/text()').extract()[2:]


        zipped = zip(sch_urls, sch_names)
        zipped = [x for x in zipped if x[0].endswith('.edu.cn')]

        sch_area = response.meta['sch_area']
        for itom in zipped:

            # print(itom)
            item = GaoxiaospiderItem()

            sch_url = itom[0]
            sch_name = itom[1]

            pattern = re.compile(r'http://(www\.)?(\w+\.)?(\w+)\.edu\.cn')
            result = pattern.search(sch_url).groups()

            sch_abbr = result[-1]
            sch_pfix = sch_abbr+'.edu.cn'

            item['sch_area'] = sch_area
            item['sch_url'] = sch_url
            item['sch_name'] = sch_name
            item['sch_pfix'] = sch_pfix
            item['sch_abbr'] = sch_abbr

            yield item

        # print(sch_urls)
        # print(sch_names)
        # sch_pfix = []
        # sch_abbr =





        # self.logger.info("start parsing")
        # self.driver.get(response.url)
        #
        # # find n images
        # xpath = r'//*[@id="imgid"]/div[*]/ul/li[*]/div[*]/a/img[@data-imgurl]'
        # n = self.number
        # i = 0
        # while i < n:
        #     # count images
        #     elems = self.driver.find_elements_by_xpath(xpath)
        #
        #     # update i
        #     if i != len(elems):
        #         i = len(elems)
        #     else:
        #         break
        #
        #     # scroll down
        #     actions = webdriver.ActionChains(self.driver)
        #     actions.move_to_element(elems[-1])  # 模拟鼠标移动到最后一个图片元素
        #     actions.perform()  # 开始执行
        #     time.sleep(0.5)  # 怕太快加载不出来
        #
        # self.logger.info("found {} image(s)".format(i))
        #
        # # save images
        # item = BaiduimageItem()
        # if elems:
        #     item["image_urls"] = [elem.get_attribute("data-imgurl") for elem in elems]
        #     item["images"] = ["{}{:04}{}".format(self.keyword, i, os.path.splitext(x)[1]) \
        #                       for i, x in enumerate(item["image_urls"])]
        #     self.logger.info("start downloading")
        #     return item

    # errors from downloader
    def error(self, failure):
        self.logger.error(repr(failure))