import re
from future.utils import lmap, lfilter


class AbodePriceProcessor(object):
    def format_price(self, price_text):
        """Take text representing a price on the abode website and return an integer."""
        return int(re.sub(r"\D", "", price_text))

    def __call__(self, values, loader_context):
        return lmap(lambda x: x*loader_context.get('number_bedrooms'), lmap(self.format_price, values))


class AbodeEpcRatingProcessor(object):

    def __call__(self, values):
        """Takes a list of property features and extracts the EPC rating"""
        epc_rating_items = lfilter(lambda v: v.startswith('EPC Rating'), values)
        return epc_rating_items[0][-1]