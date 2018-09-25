# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import time


class MySQLStorePipeline(object):
    def __init__(self):
        # self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root',db='jobs', charset="utf8mb4", use_unicode=True)
        # self.cursor = self.conn.cursor()
        pass
    def process_item(self, item, spider):
        print(item)
        # if spider.name in ['maimai', 'lagou', 'zhipin']:
        #     try:
        #         self.cursor.execute('delete from position_s where sid = %s and source = %s',
        #                             (item['id'], item['source']))  # 2:m 3:l 4:z
        #         self.cursor.execute(
        #             """INSERT INTO position_s (company, title, salary_max, salary_min, type, education, working_years, description, label, pub_name, pub_info, province, city, address, source, status, created, updated, sid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #             (item['company'], item['position'], item['salary_max'], item['salary_min'],
        #              item['type'], item['degree'], item['worktime'], item['description'], item['sup_text'],
        #              item['user_info'], item['email'], item['province'], item['city'], item['address'], item['source'],
        #              item['status'], item['pub_time'], item['uptime'], item['id']))
        #
        #         self.conn.commit()
        #     except MySQLdb.Error as e:
        #         print("Error %d: %s" % (e.args[0], e.args[1]))
        # elif spider.name == 'company':
        #     try:
        #         self.cursor.execute(
        #             """INSERT INTO company (member_id, name, fullname, logo, intro, scale, stage, industry, email, label, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #             ('0', item['abbreviation'], item['name'], item['logo'][-1] if len(item['logo']) > 0 else '',
        #              item['info'], item['size'],
        #              item['financing_situation'][-1] if len(item['financing_situation']) > 0 else '', item['industry'],
        #              item['website'],
        #              item['address'], '1'))
        #
        #         self.conn.commit()
        #     except MySQLdb.Error as e:
        #         print("Error %d: %s" % (e.args[0], e.args[1]))

        return item
