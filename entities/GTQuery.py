__author__ = 'indika'

from urlparse import urljoin

class GumtreeQuery:
    def __init__(self, base_address, location, c_id):
        self.base_address = base_address
        self.location = location
        self.c_id = c_id

    def make_url(self):
        house_share = 's-flatshare-houseshare'
        url = ''
        url = url + house_share
        url = url + '/' + self.location
        url = url + '/' + 'page-1'
        url = url + '/' + self.c_id
        url = url + '?' + 'ad=offering'
        url = url + '&' + 'price=0.00__200.00'
        url = urljoin(self.base_address, url)
        return url

    def cache_file_name(self):
        return self.location + '.html'


def test_url():
    base_address = 'http://www.gumtree.com.au'
    query = GumtreeQuery(base_address, 'west-end-brisbane', 'c18294l3005921')
    url = query.make_url()
    print url
    assert url == 'http://www.gumtree.com.au/s-flatshare-houseshare/west-end-brisbane/page-1/c18294l3005921?ad=offering&price=0.00__200.00'