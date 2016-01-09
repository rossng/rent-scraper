import re
from future.utils import lmap, lfilter

class UbuLettingsPriceProcessor(object):

    def format_price(self, price_text):
        """Take text representing a total price per month and return an integer representing cost per person per month."""
        # TODO: eliminate magic numbers
        return int(re.sub(r"\D", "", price_text))/5

    def __call__(self, values):
        return lmap(self.format_price, values)

class UbuLettingsPostcodeProcessor(object):

    def __call__(self, values):
        """Takes a link to Google maps on the UBU lettings website and converts it to a postcode"""
        # TODO: implement
        return values[0].split(',')[2].strip()


class UbuLettingsAreaProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'St Andrews Road, Montpelier, Bristol' and returns 'Montpelier'"""
        return values[0].split(',')[1].strip()

class UbuLettingsStreetProcessor(object):

    def __call__(self, values):
        """Takes a list containing a string like 'St Andrews Road, Montpelier, Bristol' and returns 'St Andrews Road'"""
        return values[0].split(',')[0].strip()

class UbuLettingsEpcRatingProcessor(object):

    def __call__(self, values):
        """Takes a list of property features and extracts the EPC rating"""
        epc_rating_items = lfilter(lambda v: v.lower().startswith('energy rating '), values)
        return epc_rating_items[0][14] if len(epc_rating_items) > 0 else "Unknown"