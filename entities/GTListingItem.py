class GTListingItem:
    """
    An individual gumtree item
    """

    def __init__(self, title, summary="", description="", thumbnail="",
                 price="", location="", adref="", url="", contact_name="",
                 contact_number="", images=[]):
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
        self.latitude = None