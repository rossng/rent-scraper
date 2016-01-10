import re
from future.utils import lmap, lfilter


class GoughPriceProcessor(object):

    def format_price(self, price_text):
        """Take text representing a price on the abode website and return an integer."""
        return int(re.sub(r"\D", "", price_text))/4 # todo: remove magic number

    def __call__(self, values):
        return self.format_price(values[0])


class GoughStreetProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'Cotham Brow - Cotham' and returns 'Cotham Brow'"""
        return values[0].split(' - ')[0].strip()


class GoughAreaProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'Cotham Brow - Cotham' and returns 'Cotham'"""
        return values[0].split(' - ')[-1].strip()