# coding=utf-8
import re

from future.utils import lmap, lfilter


class CityPropertyLetsPriceProcessor(object):
    def format_price(self, price_text):
        """Take text representing a total price per month and return an integer representing price per month."""
        match = re.search(u"Price: \u00a3([\d\.]+) per", price_text, re.IGNORECASE) # regex is 'good enough'
        return float(match.group(1)) if match else 0

    def __call__(self, values, loader_context):
        return lmap(lambda x: x*loader_context.get('number_bedrooms'), lmap(self.format_price, values))


class CityPropertyLetsNumberBedroomsProcessor(object):
    def get_bedrooms(self, text):
        tokens = text.split(" ")
        return 1 if tokens[0] == "Room" else int(tokens[0])

    def __call__(self, value):
        return self.get_bedrooms(value)