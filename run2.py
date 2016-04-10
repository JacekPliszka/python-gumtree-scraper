#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urlparse
import time

from config import config
from gumtreescraper import SearchListing
from database import session
from gumtree_item import GTItem


class SearchListingByURL(SearchListing):
    def __init__(self, config, url):
        self.config = config
        self.url = url
        self.listing_results = self.do_search_url()

searchListing = []

excluded_words = [i.lower() for i in config['excluded_words']]


def excluded_word_in(text):
    for i in excluded_words:
        if i in text:
            return True
    return False

NEXT_PAGE_LIMIT = 40
price_range = config.get("price_range", [-1, 99999999999])

for url in config['urls']:
    page = 1
    baseurl = '{0.scheme}://{0.hostname}'.format(urlparse.urlparse(url))
    while page <= NEXT_PAGE_LIMIT:
        searchListing = SearchListingByURL(config, url)
        for result in searchListing.listing_results:
            if excluded_word_in(result.title.lower()):
                continue
            if excluded_word_in(result.summary.lower()):
                continue
            if result.price.isdigit():
                price = int(result.price)
                if price < price_range[0] or price > price_range[1]:
                    continue
            matched = session.query(GTItem).filter(
                GTItem.url == result.url
            ).all()
            if len(matched) == 0:
                session.add(result)
            print(
                u"\n{0.price} {0.date} {0.title}\n{0.summary}".format(result)
            )
        session.commit()
        if not searchListing.next_page:
            break
        url = baseurl + searchListing.next_page
        page += 1
        time.sleep(30)
