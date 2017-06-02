import re

import requests
from bs4 import BeautifulSoup


def relation_extract(url):
    resp = requests.get(url, timeout=5)
    soup = BeautifulSoup(resp.text, 'lxml')

    douban_link = ''
    book_name = ''
    for tag in soup.find_all('a'):
        if tag['href'].startswith('http://book.douban.com/subject/'):
            douban_link = tag['href']

    for tag in soup.find_all('p'):
        if tag.string is not None and tag.string.startswith(u'文件名称'):
            book_name = tag.string.split('：')[1].strip()

    return douban_link, book_name


def get_list(url):
    resp = requests.get(url, timeout=5)
    soup = BeautifulSoup(resp.text, 'lxml')
    for tag in soup.find_all('a'):
        if tag['href'].startswith('http://mebook.cc/'):
            print(tag['href'])


if __name__ == '__main__':
    # relation_extract('http://mebook.cc/7780.html')
    get_list('http://mebook.cc/date/2017/06/page/2')
