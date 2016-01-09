import re
from future.utils import lmap, lfilter

class AbodePriceProcessor(object):

    def format_price(self, price_text):
        """Take text representing a price on the abode website and return an integer."""
        return int(re.sub(r"\D", "", price_text))

    def __call__(self, values):
        return lmap(self.format_price, values)

class AbodePostcodeProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'Horfield, Toronto Road, BS7 0JP' and returns 'BS7 0JP'"""
        return values[0].split(',')[2].strip()


class AbodeAreaProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'Horfield, Toronto Road, BS7 0JP' and returns 'Horfield'"""
        return values[0].split(',')[0].strip()

class AbodeStreetProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'Horfield, Toronto Road, BS7 0JP' and returns 'Toronto Road'"""
        return values[0].split(',')[1].strip()

class AbodeEpcRatingProcessor(object):

    def __call__(self, values):
        """Takes a list of property features and extracts the EPC rating"""
        epc_rating_items = lfilter(lambda v: v.startswith('EPC Rating'), values)
        return epc_rating_items[0][-1]