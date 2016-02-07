"""
python-gumtree

Gumtree scraper written in Python

Copyright 2013 Oli Allen <oli@oliallen.com>
"""

USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
REQUEST_HEADERS = {'User-agent': USER_AGENT, }

import requests
import re
from bs4 import BeautifulSoup


class SearchListing:
    """
    A gumtree search result set containing GTItem objects
    """

    def __init__(self, category, query="", location=""):
        self.category = category
        self.query = query
        self.location = location
        self.listing_results = self.do_search()

    def __str__(self):
        return "Search listing"

    def do_search(self):
        """
        Performs the search against gumtree
        """
        # % (self.query, self.location, self.category)
        request = requests.get(
            "http://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/targowek/mieszkanie/v1c9073l3200018a1dwp1",
            headers=REQUEST_HEADERS)

        if request.status_code == 200:
            # Got a valid response

            listing_results = []

            souped = BeautifulSoup(request.text, "html5lib")
            for listings_wrapper in souped.find_all("div", class_="view"):
                for listing in listings_wrapper.find_all("li", class_="result pictures"):
                    title = listing.find("div", class_="title").find("a").text
                    item_instance = GTItem(title=title)
                    item_instance.url = listing.find("div", class_="title").find("a").get("href")
                    amount_result = listing.find("span", class_="amount")
                    if amount_result is not None:
                        item_instance.price = amount_result.string
                    desc_result = listing.find("div", class_="description")
                    desc_result_span = desc_result.find("span")
                    if desc_result_span is not None:
                        item_instance.summary = desc_result_span.string
                    else:
                        item_instance.summary = desc_result.string
                    item_instance.location = listing.find("div", class_="category-location").find("span").string
                    item_instance.thumbnail = listing.find("img", class_="thumbM").get("src")
                    # item_instance.adref = listing.find("div", class_="ad-save").get("data-ad-id")

                    listing_results.append(item_instance)
            return listing_results
        else:
            # TODO: Add error handling
            print("Server returned code %s" % request.status_code)
            return []


class GTItem:
    """
    An individual gumtree item
    """

    def __init__(self, title, summary="", description="", thumbnail="", price="", location="", adref="", url="",
                 contact_name="", contact_number="", images=[]):
        self.title = title
        self.summary = summary
        self.thumbnail = thumbnail
        self.price = price
        self.location = location
        self.adref = adref
        self.url = url

        self._description = None
        self._contact_name = None
        self._contact_number = None
        self._images = None

        self._longitude = None
        self._latitude = None

    def __repr__(self):
        return 'title: %s\n price %s\n url %s\n summary %s\n' % (self.title, self.price, self.url, self.summary)

    @property
    def images(self):
        if not self._images:
            self._images = ['test', ]
        return self._images

    @property
    def description(self):
        if not self._description:
            self.getFullInformation()
        return self._description

    @property
    def contact_name(self):
        if not self._contact_name:
            self.getFullInformation()
        return self._contact_name

    @property
    def contact_number(self):
        if not self._contact_number:
            self.getFullInformation()
        return self._contact_number

    @property
    def latitude(self):
        if not self._latitude:
            self.getFullInformation()
        return self._latitude

    @property
    def longitude(self):
        if not self._longitude:
            self.getFullInformation()
        return self._longitude

    def __str__(self):
        return self.title

    def getFullInformation(self):
        """
        Scrape information from a full gumtree advert page
        """
        request = requests.get(self.url, headers=REQUEST_HEADERS)
        if request.status_code == 200:
            # Got a valid response
            souped = BeautifulSoup(request.text, "html5lib")
            description = souped.find("div", id="vip-description-text").string
            if description:
                self._description = description.strip()
            else:
                self._description = ""
            contact = souped.find(class_="phone")
            if not contact:
                self._contact_name, self._contact_number = ["", ""]
            else:
                if " on " in contact.string:
                    self._contact_name, self._contact_number = contact.string.split(" on ")
                else:
                    self._contact_name, self._contact_number = ["", contact.string]

            gmaps_link = souped.find("a", class_="open_map")
            if gmaps_link:
                self._latitude, self._longitude = re.search("center=(-?\w.*),(-?\d.*)&sensor",
                                                            gmaps_link.get("data-target")).groups()
            else:
                self._latitude, self._longitude = ["", ""]

            return
        else:
            # TODO: Add error handling
            print("Server returned code %s for %s" % (request.status_code, self.url))
            return []
