#!/usr/bin/env python
# -*- coding:utf-8 -*-

from database import session
from gumtree_item import GTItem

for item in session.query(GTItem).all():
    print(
        u'''

{0.price} {0.date}
{0.url}
{0.title}
{0.summary}'''.format(item)
    )
