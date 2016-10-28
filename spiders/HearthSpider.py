# -*- coding: utf-8 -*-
import scrapy.spiders
import logging
from scrapy import Request
import items
from scrapy.crawler import CrawlerProcess
from pipelines import HearthpwnPipeline


class HearthspiderSpider(scrapy.Spider):

    name = "HearthSpider"
    base_link = "hearthpwn.com"
    allowed_domains = ["www.hearthpwn.com"]
    start_urls = (
        'http://www.hearthpwn.com/',
    )
    download_delay = 0.1

    # Yield requests for deck list pages to parse endpoint links
    def start_requests(self):

        logging.log(logging.INFO, "Loading requests")

        for count in range(1, 1500):

            yield Request(
                    url='http://www.hearthpwn.com/decks?page=' + str(count),
                    meta={'dont_merge_cookies': True}
                )

    # 1. Parse out target links out of requested html page
    # 2. Use callback function to extract html of endpoint links
    def parse(self, response):

        logging.log(logging.INFO, "Parsing links.")

        # Set to 1-26 for each deck on deck list page, less otherwise
        for position in range(1, 26):
            deck_link = response.xpath(
                '//*[@id="decks"]/tbody/tr[' + str(position) + ']/td[1]/div/span/a/@href'
            ).extract_first()
            logging.log(logging.INFO, "Extracted " + deck_link + " from " + response.url)

            yield Request(
                url="http://www." + HearthspiderSpider.base_link + deck_link,
                callback=HearthspiderSpider.parse_links,
                dont_filter=True
            )

    # Receive html response, parse necessary data and return scrapy item.
    @staticmethod
    def parse_links(response):

        item = items.HearthpwnItem()
        item['name'] = response.xpath('//*[@id="content"]/section/header/section[2]/h2/text()').extract_first()
        item['rating'] = response.xpath(
            '//*[@id="content"]/section/header/section[1]/div[1]/form/div/div[2]/text()'
        ).extract_first()
        if "+" in item['rating']:
            item['rating'] = item['rating'].split("+")[1]

        item['url'] = response.url
        item['crafting_cost'] = response.xpath('//*[@id="content"]/section/header/section[2]/ul[3]/li[3]/span/text()').extract_first()
        if str(item['crafting_cost']) == 'None':
            item['crafting_cost'] = "-1"

        item['description'] = response.xpath(
            '//*[@id="content"]/section/div/div[1]/div/div').extract_first()

        item['author'] = response.xpath(
            '//*[@id="content"]/section/header/section[3]/ul[1]/li[1]/a//text()').extract_first()

        item['hero_class'] = response.xpath(
            '//*[@id="content"]/section/header/section[1]/span').extract_first().split('-')[1].split('"')[0]

        # Decks that do not include minions do not have minion element in html, therefore it is set to 0
        item['minion_count'] = response.xpath(
            '//*[@id="content"]/section/header/section[2]/ul[2]/li[1]/text()').extract_first()
        if str(item['minion_count']) == 'None':
            item['minion_count'] = "0"
        else:
            item['minion_count'] = item['minion_count'].split(' ')[0]

        # Decks that do not include spells do not have spell element in html, therefore it is set to 0
        item['spell_count'] = response.xpath(
            '//*[@id="content"]/section/header/section[2]/ul[2]/li[2]/text()').extract_first()
        if str(item['spell_count']) == 'None':
            item['spell_count'] = "0"
        else:
            item['spell_count'] = item['spell_count'].split(' ')[0]

        # Decks that do not include weapons do not have weapon element in html, therefore it is set to 0
        item['weapon_count'] = response.xpath(
            '//*[@id="content"]/section/header/section[2]/ul[2]/li[3]/text()').extract_first()
        logging.log(logging.WARNING, "Weapon count: " + str(item['weapon_count']))
        if str(item['weapon_count']) == 'None':
            item['weapon_count'] = "0"
        else:
            item['weapon_count'] = item['weapon_count'].split(' ')[0]

        HearthpwnPipeline.process_item(HearthpwnPipeline(), item)

        yield item


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(HearthspiderSpider)
process.start()
