import re
from future.utils import lmap

class FormatPrice(object):

    def format_price(self, price_text):
        """Take text representing a price on the abode website and return an integer."""
        return int(re.sub(r"\D", "", price_text))

    def __call__(self, values):
        return lmap(self.format_price, values)