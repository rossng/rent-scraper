import re

from future.utils import lmap, lfilter


class ChappellAndMatthewsPriceProcessor(object):
    def format_price(self, price_text):
        """Take text representing a total price per month and return an integer representing price per month."""
        return int(re.sub(r"\D", "", price_text))

    def __call__(self, values):
        return self.format_price(values[0])