import json

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

_index = "hearthpwn"
_type = "deck"


class HearthpwnPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'a')

    def process_item(self, item):

        index = {
            'index': {
                '_index': _index,
                '_type': _type,
            }
        }
        self.file.write(json.dumps(index) + '\n')
        self.file.write(json.dumps(dict(item)) + '\n')

        return item
