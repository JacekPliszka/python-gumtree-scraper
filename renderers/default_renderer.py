import logging

__author__ = 'indika'

from mako.template import Template
logger = logging.getLogger('gumtree_scraper')

class DefaultRenderer():
    def render(self, listings):
        ret = ''

        exclusion_set = set(
            line.strip() for line in open('exclusion_list.txt'))

        with open('renderers/ad.html.mako', 'r') as f:
            template = f.read()
            for listing in listings:
                if listing.ad_id in exclusion_set:
                    logger.info('Excluding item: {0}'.format(listing.ad_id))
                else:
                    rendered = Template(template).render(ad_item=listing)
                    ret = ret + rendered
            with open('cache/body-cache.html', 'w') as g:
                g.write(ret.encode('utf-8'))

        with open('renderers/listing.html.mako', 'r') as f:
            template = f.read()
            rendered = Template(template).render(body=ret)

        return rendered