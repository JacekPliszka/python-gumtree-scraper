#!/usr/bin/env python

"""TestScraper

Tests the scraper


Usage:
   test_scraper.py debug listing
   test_scraper.py debug ad

Options:
    -h --help     Show this screen.
    --version     Show version.

"""
from entities.GTListingQuery import GumtreeListingQuery
from docopt import docopt

__author__ = "Indika Piyasena"


import os, sys
import logging


logger = logging.getLogger(__name__)


class TestScraper:
    def __init__(self):
        self.configure_logging()


    def process(self):
        self.arguments = docopt(__doc__, version='TestScraper 0.2')
        logger.info('TestScraper started...')

        self.base_url = 'http://www.gumtree.com.au'

        self.query_objects = [
            GumtreeListingQuery(self.base_url, 'west-end-brisbane',
                                'c18294l3005921'),
        ]

        if self.arguments['debug']:
            if self.arguments['ad']:
                self.debug_ad()
            if self.arguments['listing']:
                self.debug_listing()
            pass


    def debug_ad(self):
        # Get the first ad in the cache

        # Need a constructor: create ad with file
        pass

    def debug_listing(self):
        query = GumtreeListingQuery(self.base_url, 'west-end-brisbane',
                                'c18294l3005921')

        print query.cache_file_name()

        pass


    def configure_logging(self):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass

    def log(self):
        pass

def test_something():
    test_scraper = TestScraper()
    test_scraper.create_record()
    assert(True)


if __name__ == "__main__":
    print "Running TestScraper in stand-alone-mode"

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    test_scraper = TestScraper()
    test_scraper.process()

