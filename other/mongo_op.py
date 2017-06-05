#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import collections
import json
import logging
import re

import pymongo
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s\t:%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

MebookInfo = collections.namedtuple('MebookInfo', ['id', 'name', 'douban_link'])


def insert_merchant_locally():
    db = pymongo.MongoClient()['mebook']
    book = db['douban_book_info']
    book.create_index([('mebook_id', pymongo.DESCENDING)], background=True, unique=True)

    infos = json.loads(codecs.open('../data/some.json', 'r', 'utf-8').read())
    # 去重
    info_set = set([MebookInfo(item['link'], item['book_name'], item['douban_link']) for item in infos])
    info_list = []
    for index, item in enumerate(info_set):
        if index % 100 == 0:
            logging.info(u'done import {} merchant'.format(index))

        info = get_book_info(item)
        if info is None:
            continue
        # info_list.append(info)
        try:
            # book.insert_many(info_list)
            book.insert_one(info)
            # info_list = []
        except Exception as err:
            logging.error(err.args)


def get_book_info(item):
    # re.M跨行 re.I大小写不敏感
    match = re.match(r'http://book.douban.com/subject/([0-9]+)', item.douban_link)
    if match:
        douban_id = match.group(1)
    else:
        return None

    try:
        # info = requests.get('https://api.douban.com/v2/book/{}'.format(douban_id), timeout=5).json()
        info = requests.get('https://m.douban.com/rexxar/api/v2/book/{}/'.format(douban_id), timeout=5).json()
        if 'title' not in info:
            return None
    except Exception as err:
        logging.error(err.args)
        return None

    info['mebook_id'] = item.id
    info['mebook_name'] = item.name
    info['interest'] = []
    return info


if __name__ == '__main__':
    insert_merchant_locally()
