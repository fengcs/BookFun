# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup

# base_info:
#
# https://api.douban.com/v2/book/26986954
#
# 评论：
#
# https://m.douban.com/rexxar/api/v2/book/26279019/interests?count=10&order_by=hot&start=0
#
# related:
#
# none


def parse_book_info(url):
    resp = requests.get(url, timeout=5)
    soup = BeautifulSoup(resp.text, 'lxml')
    rating = soup.find('p', attrs={'class':'rating'})
    base_info = soup.find('p', attrs={'class':'meta'})
    print(rating.string)


if __name__ == '__main__':
    test_url = 'https://m.douban.com/book/subject/26986954/?refer=home'
    parse_book_info(test_url)



