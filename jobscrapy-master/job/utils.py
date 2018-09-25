#!/usr/bin/env python
# coding=utf-8

from datetime import datetime, timedelta

class Utils(object):
    province_city = {
        u'北京': u'北京',
        u'上海': u'上海',
        u'广州': u'广东',
        u'深圳': u'广东',
        u'杭州': u'浙江',
        u'天津': u'天津',
        u'西安': u'陕西',
        u'苏州': u'江苏',
        u'武汉': u'湖北',
        u'厦门': u'福建',
        u'长沙': u'湖南',
        u'成都': u'四川'
    }

    industry_list = {
        u'IT互联网': 10,
        u'移动互联网': 11,
        u'社交网络': 12,
        u'电子商务': 13,
        u'信息安全': 14,
        u'数据服务': 15,
        u'互联网': 16,
        u'计算机软件': 17,
        u'智能硬件': 18,
        u'互联网金融': 20,
        u'金融': 50,
    }

    @classmethod
    def valid_date(cls, dt):
        return (datetime.now() - dt).days <= 1

    @classmethod
    def sarlary_transform(cls, s):
        if 'K' in s or 'k' in s:
            return int(s[:-1]) * 1000
        elif 'W' in s or 'w' in s:
            return int(s[:-1]) * 10000

    @classmethod
    def get_province_from_city(cls, city):
        return cls.province_city[city]

    @classmethod
    def get_lagou_datetime(cls, publish_time):
        cur_day = datetime.now()
        hour = cur_day.hour
        minute = cur_day.minute

        if ':' in publish_time:
            hour = int(publish_time[0:5].split(':')[0])
            minute = int(publish_time[0:5].split(':')[1])
        elif u'天' in publish_time:
            return cur_day + timedelta(days=-(int(publish_time[:1])))

        return datetime(cur_day.year, cur_day.month, cur_day.day, hour, minute, 0, 0)

    @classmethod
    def get_zhipin_datetime(cls, publish_time):
        cur_day = datetime.now()
        year = cur_day.year
        month = cur_day.month
        day = cur_day.day
        hour = cur_day.hour
        minute = cur_day.minute

        if ':' in publish_time:
            hour = int(publish_time[3:].split(':')[0])
            minute = int(publish_time[3:].split(':')[1])
        elif u'昨天' in publish_time:
            return cur_day + timedelta(days = -1)
        elif u'月' in publish_time and u'日' in publish_time:
            month = int(publish_time[3:5])
            day = int(publish_time[6:-1])
            if month > cur_day.month or \
                    (month == cur_day.month and day >= cur_day.day):
                year = cur_day.year - 1

        return datetime(year, month, day, hour, minute, 0, 0)
