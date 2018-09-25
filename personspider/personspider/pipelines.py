# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  codecs
import  json

class JsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('result_doc.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()

# class FilePipeLine(object):
#     def __init__(self):
#         self.file = codecs.open('result.json', 'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         content = json.dumps(dict(item), ensure_ascii=False) + "\n"
#         self.file.write(content)
#         return item
#
#     def close_spider(self, spider):
#         self.file.close()
#
#     def file_path(self, request, response=None, info=None):
#
#         path = urlparse(request.url).path
#
#         return join('full', basename(dirname(path)) + ".apk")
