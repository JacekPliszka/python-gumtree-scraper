#!/usr/bin/env python

"""GumtreeScraper

Gumtree scraper written in Python.
Specifically built form finding house-share.

Derived from
Copyright 2013 Oli Allen <oli@oliallen.com>


Usage:
   gumtree_scraper.py
   gumtree_scraper.py --load-from-cache
   gumtree_scraper.py --debug-ad
   gumtree_scraper.py --output <output_file>

Options:
    -h --help     Show this screen.
    --version     Show version.


"""
from entities.GTAd import GTAd

from entities.GTListing import GTListing
from entities.GTListingQuery import GumtreeListingQuery
from entities.GTQuery import GumtreeAdQuery
from renderers.default_renderer import DefaultRenderer

__author__ = "Indika Piyasena"

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"

REQUEST_HEADERS = {'User-agent': USER_AGENT, }

import os
import logging
import requests
import pytz
import datetime
import time
import random

from tzlocal import get_localzone
from bs4 import BeautifulSoup
from docopt import docopt

logger = logging.getLogger('gumtree_scraper')

class GumtreeScraper:
    def __init__(self):
        self.configure_logging()
        self.arguments = docopt(__doc__, version='GumtreeScraper 0.2')

        self.base_url = 'http://www.gumtree.com.au'

        self.query_objects = [
            GumtreeListingQuery(self.base_url, 'west-end-brisbane',
                                'c18294l3005921', page=1),
            GumtreeListingQuery(self.base_url, 'west-end-brisbane',
                                'c18294l3005921', page=2),
            GumtreeListingQuery(self.base_url, 'toowong-brisbane',
                                'c18294l3005815'),
            GumtreeListingQuery(self.base_url, 'highgate-hill-brisbane',
                                'c18294l3005884'),
            GumtreeListingQuery(self.base_url, 'spring-hill-brisbane',
                                'c18294l3005758'),
            GumtreeListingQuery(self.base_url, 'milton-brisbane',
                                'c18294l3005798'),
            GumtreeListingQuery(self.base_url, 'auchenflower-brisbane',
                                'c18294l3005770'),
        ]

    def process(self):
        if self.arguments['--debug-ad']:
            logger.debug('Debugging an ad')
            with open('cache/item_one.cache', 'r') as f:
                self.parse_ad(f.read())
            exit(0)

        listings = []

        for query in self.query_objects:
            listings = listings + self.fetch_listings(query)

        default_renderer = DefaultRenderer()

        if self.arguments['--output']:
            output_file = self.arguments['<output_file>']
        else:
            output_file = 'output/feed.html'

        with open(output_file, 'w') as f:
            f.write(str(datetime.datetime.now()))
            rendered = default_renderer.render(listings)
            f.write(rendered.encode('utf-8').strip())
        pass

    def fetch_listings(self, listing_query):
        cache_file = 'cache/' + listing_query.cache_file_name()

        if self.arguments['--load-from-cache']:
            logger.debug(
                'Loading from cache: {0}'.format(listing_query.location))
            with open(cache_file, 'r') as f:
                content = f.read()
        else:
            url = listing_query.make_url()
            logger.info('Fetching: {0}'.format(listing_query.location))
            logger.info('Fetching: {0}'.format(url))
            
            request = requests.get(url, headers=REQUEST_HEADERS)
            content = request.content
            with open(cache_file, 'w') as f:
                f.write(content)
            self.sleep()

        listings = self.parse(content, listing_query)
        for listing in listings:
            ad_query = GumtreeAdQuery(listing.url)
            gt_ad = self.fetch_ad(ad_query)
            listing.body_raw = gt_ad.main_content
            listing.features_raw = gt_ad.features
            listing.ad_id = gt_ad.ad_id
        return listings

    def fetch_ad(self, ad_query):
        gt_ad = GTAd(ad_query)
        gt_ad.populate()
        return gt_ad

    def parse(self, content, query_object):
        logger.debug('Creating a beautiful soup...')
        souped = BeautifulSoup(content, "html5lib")

        query = souped.find_all("div", {"class": "rs-ad-field",
                                        "class": "rs-ad-detail"})

        logger.debug('Number of listings: {0}'.format(len(query)))

        result_set = []

        for listing in query:
            title = listing.find("a", class_="rs-ad-title").contents[0]
            gt_listing = GTListing(title=title)
            gt_listing.url = self.base_url + listing. \
                find("a", class_="rs-ad-title").get("href")
            gt_listing.summary = listing.find("p",
                                              class_="word-wrap").contents[0]
            gt_listing.listing_query = query_object
            result_set.append(gt_listing)

        return result_set

    def process_listing_item(self, listing_item):
        print listing_item.url
        request = requests.get(listing_item.url, headers=REQUEST_HEADERS)

        with open('cache/item_one.cache', 'w') as f:
            f.write(request.content)

        content = request.content
        result_tuple = self.parse_ad(content)
        listing_item.body_raw = result_tuple[0]
        listing_item.features_raw = result_tuple[1]
        pass

    def sleep(self):
        random_time = random.randint(3, 20)
        logger.debug('Sleeping for: {0} seconds...'.format(random_time))
        time.sleep(random_time)
        pass

    def configure_logging(self):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass


if __name__ == "__main__":
    print "Running GumtreeScraper in stand-alone-mode"

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    #server_tz = pytz.timezone("UTC")
    server_tz = get_localzone()
    local_tz = pytz.timezone("Australia/Brisbane")

    typical_datetime_object = datetime.datetime.now()
    now_server = server_tz.localize(typical_datetime_object)
    now_local = now_server.astimezone(server_tz)
    print now_local

    gumtree_scraper = GumtreeScraper()
    gumtree_scraper.process()
