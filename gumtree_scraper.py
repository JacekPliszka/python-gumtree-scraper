#!/usr/bin/env python

"""GumtreeScraper

Gumtree scraper written in Python

Derived from
Copyright 2013 Oli Allen <oli@oliallen.com>


Usage:
   gumtree_scraper.py
   gumtree_scraper.py --load-from-cache

Options:
    -h --help     Show this screen.
    --version     Show version.


"""

__author__ = "Indika Piyasena"

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"

REQUEST_HEADERS = {'User-agent': USER_AGENT,}

import os, sys
import logging
import requests
import re
import pytz
import datetime

from bs4 import BeautifulSoup
from docopt import docopt

logger = logging.getLogger(__name__)


class GumtreeScraper:
    def __init__(self, category, query="", location=""):
        self.configure_logging()
        self.arguments = docopt(__doc__, version='GumtreeScraper 0.1')

        self.category = category
        self.query = query
        self.location = location

        self.data = []
        self.cache_file = 'request.cache'

        self.base_url = 'http://www.gumtree.com.au'


    def process(self):
        self.listing_results = self.doSearch()
        print self.listing_results
        pass

    def doSearch(self):
        """
        Performs the search against gumtree
        """

        if self.arguments['--load-from-cache']:
            with open(self.cache_file, 'r') as f:
                content = f.read()

        else:
            #request = requests.get("http://www.gumtree.com.au/search?q=%s&search_location=%s&category=%s" % (self.query, self.location, self.category), headers=REQUEST_HEADERS)
            url = "{0}/s-flatshare-houseshare/west-end-brisbane/page-1/c18294l3005921?ad=offering&price=0.00__200.00".format(self.base_url)
            logger.debug('Query URL: {0}'.format(url))
            request = requests.get(url, headers=REQUEST_HEADERS)

            with open(self.cache_file, 'w') as f:
                f.write(request.content)
                content = request.content

        self.parse(content)


    def parse(self, content):
        logger.debug('Souping')
        souped = BeautifulSoup(content, "html5lib")
        logger.debug('Souping complete')

        listing_query = souped.find_all("div", { "class" : "rs-ad-field", "class" : "rs-ad-detail"})

        logger.debug('Number of listings: {0}'.format(len(listing_query)))

        for listing in listing_query:
            title = listing.find("a", class_="rs-ad-title").contents
            item_instance = GTItem(title=title)
            item_instance.url = self.base_url + listing.find("a", class_="rs-ad-title").get("href")
            item_instance.summary = listing.find("p", class_="word-wrap").contents

            print listing
            print '<a href="{0}">Link</a>'.format(item_instance.url)


    def configure_logging(self):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass


class GTItem:
    """
    An individual gumtree item
    """
    def __init__(self, title, summary="", description="", thumbnail="", price="", location="", adref="", url="", contact_name="", contact_number="", images=[]):
        self.title = title
        self.summary = summary
        self.thumbnail = thumbnail
        self.price = price
        self.location = location
        self.adref = adref
        self.url = url

        self._description = None
        self._contact_name = None
        self._contact_number = None
        self._images = None

        self._longitude = None
        self.latitude = None


if __name__ == "__main__":
    print "Running GumtreeScraper in stand-alone-mode"

    local_tz = pytz.timezone("Australia/Brisbane")
    print local_tz.localize(datetime.datetime.now())

    gumtree_scraper = GumtreeScraper('s-flatshare-houseshare')
    gumtree_scraper.process()
