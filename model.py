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

    def __init__(self, text, category, sites, use_exact_match=True, include_description=True, auction_only=True):
        self.text = text
        self.use_exact_match = use_exact_match
        self.include_description = include_description
        self.auction_only = auction_only
        self.category = category
        self.sites = sites

    def get_searchable_text(self):
        return "\"" + self.text + "\"" if self.use_exact_match else self.text

    def get_searchable_listing_type(self):
        return "Auction" if self.auction_only else "All"

    def __str__(self):
        return str(self.__dict__)


class EmailConfig:

    def __init__(self, email_from, email_to, email_title):
        self.email_from = email_from
        self.email_to = email_to
        self.email_title = email_title


class SearchConfig:

    def __init__(self, search_default_category, search_default_sites):
        self.search_default_category = search_default_category
        self.search_default_sites = search_default_sites


class Config:

    def __init__(self, email_config, search_config):
        self.email_config = email_config
        self.search_config = search_config
