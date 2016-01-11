import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join, MapCompose

from rent_scraper.processors.common_processors import TextSearch, Concatenate, Split, Get


def format_price(price_text, loader_context):
    """Take text representing a price on the Flatline website and return an integer."""
    return int(re.sub(r"\D", "", price_text)) * loader_context.get('number_bedrooms')


def to_number_bedrooms(text):
    return int(text.split(" ")[0])


class FlatlinePropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Compose(Split(' - '), Get(0), Get(1))

    street_name_in = Compose(Split(' - '), Get(0), Get(1))

    postcode_in = Identity()

    number_bedrooms_in = MapCompose(to_number_bedrooms)

    price_per_month_in = Compose(TakeFirst(), MapCompose(format_price))

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    let_agreed_in = Compose(lambda xs: 'Yes' if any('Let' in x for x in xs) else 'No')