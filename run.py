#!/usr/bin/python
import sys

from gumtreescraper import SearchListing
from database import session, Base, engine
from gumtree_item import GTItem

Base.metadata.create_all(engine)

searchListing = SearchListing(sys.argv[1], sys.argv[2], sys.argv[3])

for result in searchListing.listing_results:
    matched = session.query(GTItem).filter(GTItem.url == result.url).all()
    if len(matched) == 0:
        session.add(result)

session.commit()

from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.title('Gumtree feed')
fg.description('Gumtree feed')
fg.link(href='http://example.com', rel='alternate')


all_result = session.query(GTItem).order_by(GTItem.creation_date.desc()).limit(1000).all()

for result in all_result:
    fe = fg.add_entry()
    url = 'http://www.gumtree.pl' + result.url
    fe.id(url)
    fe.link(href=url, rel='alternate')
    fe.title(result.price + ' ' + result.title)
    fe.description(result.summary)

fg.rss_file('rss.xml')
