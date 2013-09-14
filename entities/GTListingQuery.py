from urlparse import urljoin


class GumtreeListingQuery:
    def __init__(self, base_address, location, c_id, page=1):
        self.base_address = base_address
        self.location = location
        self.c_id = c_id
        self.page = 'page-{0}'.format(page)

    def make_url(self):
        house_share = 's-flatshare-houseshare'
        url = ''
        url += house_share
        url = url + '/' + self.location
        url = url + '/' + self.page
        url = url + '/' + self.c_id
        url = url + '?' + 'ad=offering'
        url = url + '&' + 'price=0.00__200.00'
        url = urljoin(self.base_address, url)
        return url

    def cache_file_name(self):
        return '{}-{}.html'.format(self.location, self.page)
