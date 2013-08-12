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
            url = "http://www.gumtree.com.au/s-flatshare-houseshare/west-end-brisbane/page-1/c18294l3005921?ad=offering&price=0.00__200.00"
            logger.debug('Query URL: {0}'.format(url))
            request = requests.get(url, headers=REQUEST_HEADERS)

            with open(self.cache_file, 'w') as f:
                f.write(request.content)
                content = request.content

        self.parse(content)

        #self.data = request.content
        #self.pickle()
        exit(0)

        if request.status_code == 200:
            # Got a valid response

            listing_results = []

            souped = BeautifulSoup(request.text, "html5lib")
            for listings_wrapper in souped.find_all("ul", class_="ad-listings"):
                for listing in listings_wrapper.find_all("li", class_="offer-sale"):
                    title = listing.find("a", class_="description").get("title")
                    item_instance = GTItem(title=title)
                    item_instance.url = listing.find("a", class_="description").get("href")
                    item_instance.price = listing.find("span", class_="price").string
                    item_instance.summary = listing.find("div", class_="ad-description").find("span").string
                    item_instance.location =  listing.find("span", class_="location").string
                    item_instance.thumbnail = listing.find("img", class_="thumbnail").get("src")
                    item_instance.adref = listing.find("div", class_="ad-save").get("data-ad-id")

                    listing_results.append(item_instance)
            return listing_results
        else:
            # TODO: Add error handling
            print "Server returned code %s" % request.status_code
            return []

    def parse(self, content):
        logger.debug('souping')
        souped = BeautifulSoup(content, "html5lib")
        logger.debug('done souping')
        #for listings_wrapper in souped.find_all("div", class_="rs-ad-field rs-ad-detail"):

        listing_query = souped.find_all("div", { "class" : "rs-ad-field", "class" : "rs-ad-detail"})

        logger.debug('Number of listings: {0}'.format(len(listing_query)))

        for listings_wrapper in listing_query:
            print listings_wrapper


    def configure_logging(self):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass


if __name__ == "__main__":
    print "Running GumtreeScraper in stand-alone-mode"
    gumtree_scraper = GumtreeScraper('s-flatshare-houseshare')
    gumtree_scraper.process()
