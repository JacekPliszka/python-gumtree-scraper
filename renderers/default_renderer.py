__author__ = 'indika'

from mako.template import Template

class DefaultRenderer():

    def render(self, ad_items):
        ret = ''
        with open('renderers/ad.html.mako', 'r') as f:
            template = f.read()
            for ad_item in ad_items:
                rendered = Template(template).render(ad_item=ad_item)
                # ret = ret + rendered.encode('utf-8').strip()
                ret = ret + rendered

        with open('renderers/listing.html.mako', 'r') as f:
            template = f.read()
            rendered = Template(template).render(body=ret)

        return rendered