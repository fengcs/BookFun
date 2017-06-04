# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup
import scrapy
from crawl.items import BookItem


class BookSpider(scrapy.Spider):
    name = 'mebook'
    allowed_domains = ['mebook.cc']
    start_urls = ['http://mebook.cc/', ]

    item_reg = re.compile('http://mebook.cc/([0-9]+).html')

    def parse(self, response):
        result = re.match(self.item_reg, response.url)
        if result:
            book_name, douban_link = self.parse_item(response)
            if douban_link != '' and book_name != '':
                print(result.group(1), douban_link, book_name)
                yield BookItem(link=result.group(1), douban_link=douban_link, book_name=book_name)

        for url in response.xpath('//a/@href').extract():
            print(url)
            if not url.startswith('http://mebook.cc/'):
                continue
            # yield response.follow(url, callback=self.parse)
            yield scrapy.Request(url, callback=self.parse)

    def parse_item(self, respone):
        soup = BeautifulSoup(respone.text, 'lxml')

        douban_link = ''
        book_name = ''
        for tag in soup.find_all('a'):
            if tag['href'].startswith('http://book.douban.com/subject/'):
                douban_link = tag['href']

        for tag in soup.find_all('p'):
            if tag.string is not None and tag.string.startswith(u'文件名称'):
                book_name = tag.string.split('：')[1].strip()

        return book_name, douban_link