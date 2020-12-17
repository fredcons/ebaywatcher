from model import SearchResult
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from orderedset import OrderedSet


class Search:

    def __init__(self, search_config):
        self.ebay_app_id = search_config.ebay_app_id

    def search(self, date, search_definitions):
        all_results = OrderedSet()
        for search_definition in search_definitions:
            results = self.single_search(date, search_definition)
            print("Search for %s gave %s results" % (search_definition.text, str(len(results))))
            all_results.update(results)
        return all_results

    def single_search(self, date, search_definition):
        all_results = OrderedSet()
        for ebay_site in search_definition.sites:
            all_results.update(self.single_site_search(ebay_site, date, search_definition))
        return all_results

    def single_site_search(self, site, start_date, search_definition):

        results = set()

        try:
            api = Connection(siteid=site, appid=self.ebay_app_id, config_file=None, https=True)

            api_request = {
                'keywords': search_definition.get_searchable_text(),
                'descriptionSearch': str(search_definition.include_description).lower(),
                'categoryId': search_definition.category,
                'itemFilter': [
                    {'name': 'ListingType', 'value': search_definition.get_searchable_listing_type()},
                    {'name': 'StartTimeFrom', 'value': start_date}
                ]
            }

            response = api.execute('findItemsAdvanced', api_request)

            if int(response.reply.searchResult._count) > 0:
                for item in response.reply.searchResult.item:
                    results.add(SearchResult(item.itemId,
                                             item.title,
                                             item.primaryCategory.categoryName,
                                             "{:.2f}".format(float(item.sellingStatus.currentPrice.value)),
                                             item.sellingStatus.currentPrice._currencyId,
                                             getattr(item, 'galleryURL', ''),
                                             item.viewItemURL,
                                             item.listingInfo.endTime,
                                             search_definition.text))
            #        print(response.reply.searchResult.item[0])
            # else: print("No result")

        except ConnectionError as e:
            print(e)
            print(e.response.dict())

        return results
