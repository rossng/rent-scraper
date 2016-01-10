import re
from future.utils import lmap, lfilter


class AbsolutePriceProcessor(object):

    def format_price(self, price_text):
        """Take text representing a price on the abode website and return an integer."""
        return int(re.sub(r"\D", "", price_text))/4 # todo: remove magic number

    def __call__(self, values):
        return self.format_price(values[1])


class AbsolutePostcodeProcessor(object):
    #todo
    def __call__(self, values):
        """Takes a list containing a string like 'Horfield, Toronto Road, BS7 0JP' and returns 'BS7 0JP'"""
        return values[0].split(',')[2].strip()


class AbsoluteStreetProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'Horfield, Toronto Road, BS7 0JP' and returns 'Toronto Road'"""
        return values[0].split(',')[1].strip()


class AbsoluteEpcRatingProcessor(object):
    #todo
    def __call__(self, values):
        return 'unknown'
        #epc_rating_items = lfilter(lambda v: v.startswith('EPC Rating'), values)
        #return epc_rating_items[0][-1]