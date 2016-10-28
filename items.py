# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HearthpwnItem(scrapy.Item):

    # define the fields for your item here like:
    name = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()
    crafting_cost = scrapy.Field()
    hero_class = scrapy.Field()
    author = scrapy.Field()
    minion_count = scrapy.Field()
    spell_count = scrapy.Field()
    weapon_count = scrapy.Field()
    description = scrapy.Field()

