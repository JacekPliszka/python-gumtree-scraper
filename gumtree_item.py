import datetime
from sqlalchemy import Column, Integer, String, DateTime

from database import Base


__author__ = 'jtomaszk'


class GTItem(Base):
    __tablename__ = 'gt_item'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(String)
    summary = Column(String)
    thumbnail = Column(String)
    price = Column(String)
    location = Column(String)
    adref = Column(String)
    url = Column(String)
    creation_date = Column(DateTime)

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
        self.creation_date = datetime.datetime.now()

        self.date = ''
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

    # def getFullInformation(self):
    #     """
    #     Scrape information from a full gumtree advert page
    #     """
    #     request = requests.get(self.url, headers=REQUEST_HEADERS)
    #     if request.status_code == 200:
    #         # Got a valid response
    #         souped = BeautifulSoup(request.text, "html5lib")
    #         description = souped.find("div", id="vip-description-text").string
    #         if description:
    #             self._description = description.strip()
    #         else:
    #             self._description = ""
    #         contact = souped.find(class_="phone")
    #         if not contact:
    #             self._contact_name, self._contact_number = ["", ""]
    #         else:
    #             if " on " in contact.string:
    #                 self._contact_name, self._contact_number = contact.string.split(" on ")
    #             else:
    #                 self._contact_name, self._contact_number = ["", contact.string]
    #
    #         gmaps_link = souped.find("a", class_="open_map")
    #         if gmaps_link:
    #             self._latitude, self._longitude = re.search("center=(-?\w.*),(-?\d.*)&sensor",
    #                                                         gmaps_link.get("data-target")).groups()
    #         else:
    #             self._latitude, self._longitude = ["", ""]
    #
    #         return
    #     else:
    #         # TODO: Add error handling
    #         print("Server returned code %s for %s" % (request.status_code, self.url))
    #         return []
