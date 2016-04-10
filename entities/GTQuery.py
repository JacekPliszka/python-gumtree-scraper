__author__ = 'indika'







class GumtreeAdQuery:
    def __init__(self, url):
        self.url = url

    def cache_file_name(self):
        return self.url.replace("/", "_") + '.html'


def test_url():
    base_address = 'http://www.gumtree.com.au'
    query = GumtreeListingQuery(base_address, 'west-end-brisbane',
                                'c18294l3005921')
    url = query.make_url()
    print url
    assert url == 'http://www.gumtree.com.au/s-flatshare-houseshare/west-end-brisbane/page-1/c18294l3005921?ad=offering&price=0.00__200.00'

def test_ad_cache_name():
    ad_query = GumtreeAdQuery('http://www.gumtree.com.au/s-ad/west-end/flatshare-houseshare/west-end-200pw-incl-bills-and-internet/1025791617')
    print ad_query.cache_file_name()