"""
python-gumtree

Gumtree scraper written in Python

Copyright 2013 Oli Allen <oli@oliallen.com>
"""
from gumtree_item import GTItem

USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
REQUEST_HEADERS = {'User-agent': USER_AGENT, }

import requests
from bs4 import BeautifulSoup


class SearchListing:
    """
    A gumtree search result set containing GTItem objects
    """

    def __init__(self, config, category, query="", location=""):
        self.category = category
        self.query = query
        self.location = location
        self.listing_results = self.do_search()

    def __str__(self):
        return "Search listing"

    def do_search_url(self):
        request = requests.get(self.url, headers=REQUEST_HEADERS)

        if request.status_code == 200:
            # Got a valid response

            listing_results = []
            souped = BeautifulSoup(request.text, "html5lib")
            try:
                self.next_page = souped.find("a", class_="next follows").attrs['href']
            except Exception as e:
                self.next_page = None
            for listings_wrapper in souped.find_all("div", class_="view"):
                for listing in listings_wrapper.find_all("li", class_="result pictures"):
                    title = listing.find("div", class_="title").find("a").text
                    item_instance = GTItem(title=title)
                    item_instance.url = listing.find("div", class_="title").find("a").get("href")
                    amount_result = listing.find("span", class_="amount")
                    if amount_result is not None:
                        price = amount_result.string.replace(u'\xa0', '')
                        item_instance.price = price.replace(u'z\u0142', '').strip()
                    desc_result = listing.find("div", class_="description")
                    desc_result_span = desc_result.find("span")
                    if desc_result_span is not None:
                        item_instance.summary = desc_result_span.string
                    else:
                        item_instance.summary = desc_result.string
                    item_instance.location = listing.find(
                        "div",
                        class_="category-location"
                    ).find("span").string
                    item_instance.summary = item_instance.summary.strip()
                    item_instance.thumbnail = listing.find("img", class_="thumbM").get("src")
                    # item_instance.adref = listing.find("div", class_="ad-save").get("data-ad-id")

                    creation_date_div = listing.find("div", class_="creation-date")
                    if creation_date_div:
                        item_instance.date = ' '.join(
                            i.text for i in creation_date_div.find_all('span')
                        ).strip()
                    listing_results.append(item_instance)
            return listing_results
        else:
            # TODO: Add error handling
            print("Server returned code %s" % request.status_code)
            return []

    def do_search(self):
        """
        Performs the search against gumtree
        """
        url_fmt = "{0.config[baseurl]}/{0.category}/{0.query}/{0.location}"
        self.url = url_fmt.format(self)
        return self.do_search_url()
