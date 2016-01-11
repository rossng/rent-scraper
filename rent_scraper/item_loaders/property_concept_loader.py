import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join, MapCompose

from rent_scraper.processors.common_processors import TextSearch, Concatenate, Split, Get


def format_price(price_text):
    """Take text representing a price on the Ocean website and return an integer."""
    return int(re.sub(r"\D", "", price_text))


def to_epc_rating(text):
    match_or_none = re.search("EPC( band)?: (.)", text, re.IGNORECASE)
    return match_or_none.group(2) if match_or_none else None


class PropertyConceptPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Compose(Split(','), Get(0), Get(1))

    street_name_in = Compose(Split(','), Get(0), Get(0))

    postcode_in = Identity()

    number_bedrooms_in = Compose(TakeFirst(), MapCompose(int))
    number_bathrooms_in = Compose(TakeFirst(), MapCompose(int))

    price_per_month_in = Compose(TakeFirst(), MapCompose(format_price))

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    let_agreed_in = Compose(lambda xs: 'Let' if any('Let Agreed' in x for x in xs) else 'No')

    epc_rating_in = Compose(MapCompose(to_epc_rating), lambda xs: filter(lambda x: x, xs))