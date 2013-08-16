__author__ = 'indika'

from mako.template import Template

class DefaultRenderer():

    def render(self, ad_items):
        ret = ''
        with open('renderers/ad.html', 'r') as f:
            template = f.read()
            for ad_item in ad_items:
                # print ad_item.title
                rendered = Template(template).render(ad_item=ad_item)
                ret = ret + rendered.encode('utf-8').strip()
        return ret