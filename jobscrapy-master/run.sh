#!/bin/bash

cd /home/zhoufan/jobscrapy
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl maimai

scrapy crawl lagou

#rm proxy.json
#scrapy crawl proxy -a api='http://webapi.http.zhimacangku.com/getip?num=20&type=2&pro=&city=0&yys=0&port=11&pack=11672&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=' -o proxy.json
#scrapy crawl zhipin

mv scrapy.log scrapy.log.$(date "+%Y-%m-%d")
