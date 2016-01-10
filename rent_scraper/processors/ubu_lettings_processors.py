import re
from future.utils import lmap, lfilter

class UbuLettingsPriceProcessor(object):

    def format_price(self, price_text):
        """Take text representing a total price per month and return an integer representing cost per person per month."""
        # TODO: eliminate magic numbers
        return int(re.sub(r"\D", "", price_text))

    def __call__(self, values):
        return lmap(self.format_price, values)

class UbuLettingsEpcRatingProcessor(object):

    def __call__(self, values):
        """Takes a list of property features and extracts the EPC rating"""
        epc_rating_items = lfilter(lambda v: v.lower().startswith('energy rating '), values)
        return epc_rating_items[0][14] if len(epc_rating_items) > 0 else "Unknown"