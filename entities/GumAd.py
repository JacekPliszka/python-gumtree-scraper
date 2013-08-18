import logging
import os
import requests
import time
from bs4 import BeautifulSoup

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"

REQUEST_HEADERS = {'User-agent': USER_AGENT, }
logger = logging.getLogger('gumtree_scraper')


class GumAd:
    """
    An individual gumtree ad
    """

    def __init__(self, ad_query):
        self.ad_query = ad_query
        self.ad_id = None

    def populate(self):
        ad_query = self.ad_query
        cache_file = 'cache/' + ad_query.cache_file_name()
        if os.path.exists(cache_file):
            logger.debug('Loading from cache: {0}'.format(ad_query.url))
            with open(cache_file, 'r') as f:
                content = f.read()
        else:
            logger.debug('Fetching: {0}'.format(ad_query.url))
            request = requests.get(ad_query.url, headers=REQUEST_HEADERS)
            content = request.content
            with open(cache_file, 'w') as f:
                f.write(content)
            self.sleep()
        return self.parse_ad(content)

    def parse_ad(self, ad_content):
        logger.debug('Souping ad')
        souped = BeautifulSoup(ad_content, "html5lib")
        main_box = souped.find("div", {"class": "white-box"})
        main_content = main_box.find("p", {"id": "vip-description"})
        features = main_box.find("div", {"id": "vip-ad-attr-features"})
        return main_content, features

    # def set_id(self):
    #     self.ad_id = self.url.substr(self.url.lastIndexOf("/") + 1)

    def sleep(self):
        random_time = 5
        logger.debug('Sleeping for: {0} seconds...'.format(random_time))
        time.sleep(random_time)
        pass