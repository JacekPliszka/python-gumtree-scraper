import logging
import os
import re
import requests
import time
from bs4 import BeautifulSoup

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"

REQUEST_HEADERS = {'User-agent': USER_AGENT, }
logger = logging.getLogger('gumtree_scraper')


class GTAd:
    """
    An individual gumtree ad
    """

    def __init__(self, ad_query):
        self.ad_query = ad_query
        self.ad_id = None
        self.main_content = None
        self.features = None

    def populate(self):
        ad_query = self.ad_query
        self.ad_id = self.obtain_id_from_url(ad_query.url)

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
        self.main_content, self.features = self.interpret_content(content)

    def interpret_content(self, ad_content):
        logger.debug('Souping ad')
        souped = BeautifulSoup(ad_content, "html5lib")
        is_expired = souped.find("div", {"id": "expiredAd"})
        if is_expired:
            return None, None
        else:
            main_box = souped.find("div", {"class": "white-box"})
            main_content = main_box.find("p", {"id": "vip-description"})
            features = main_box.find("div", {"id": "vip-ad-attr-features"})
            return main_content, features

    def sleep(self):
        random_time = 5
        logger.debug('Sleeping for: {0} seconds...'.format(random_time))
        time.sleep(random_time)
        pass

    def obtain_id_from_url(self, url):
        regex = re.compile(".*/(.*)", re.UNICODE)
        results = regex.findall(url)
        if len(results) == 1:
            return results[0]
        else:
            raise NameError('Failed to obtain ad id from URL')
        pass


def test_id_extraction():
    u_string = unicode(
        'http://www.gumtree.com.au/s-ad/toowong/flatshare-houseshare/room-in-toowong-available-now-/1025671960',
        'utf_8')
    gum_ad = GTAd(None)
    ad_id = gum_ad.obtain_id_from_url(u_string)
    assert ad_id == '1025671960'
