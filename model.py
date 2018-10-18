class SearchResult:

    def __init__(self, id, title, category_name, price, currency, image_url, item_url, end_time):
        self.id = id
        self.title = title
        self.category_name = category_name
        self.price = price
        self.currency = currency
        self.image_url = image_url
        self.item_url = item_url
        self.end_time = end_time

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class SearchDefinition:

    def __init__(self, text, use_exact_match=True, include_description=True, auction_only=True):
        self.text = text
        self.use_exact_match = use_exact_match
        self.include_description = include_description
        self.auction_only = auction_only

    def get_searchable_text(self):
        return "\"" + self.text + "\"" if self.use_exact_match else self.text

    def get_searchable_listing_type(self):
        return "Auction" if self.auction_only else "All"

    def __str__(self):
        return str(self.__dict__)
