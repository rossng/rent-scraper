import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join, MapCompose

from rent_scraper.processors.common_processors import TextSearch, Concatenate, Get, Split


def to_price_per_month(price_text, loader_context):
    """Take text representing a total price per month and return an integer representing price per month."""
    num_bedrooms = loader_context.get('number_bedrooms')
    return float(re.sub(r"[^\d\.]", "", price_text)) * (52.0 / 12.0) * (float(num_bedrooms) if num_bedrooms else 0)

def to_number_bedrooms(text):
    tokens = text.split(", ")
    bedroom_tokens = tokens[1].split(" ")
    return int(bedroom_tokens[0]) if bedroom_tokens else 0


def to_epc_rating(text):
    match_or_none = re.search("EPC Rating (.)", text, re.IGNORECASE)
    return match_or_none.group(1) if match_or_none else None


class JacksonPropertyPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Identity()

    street_in = MapCompose(Split(' - '), Get(0), Get(0))

    price_per_month_in = Compose(TakeFirst(), MapCompose(to_price_per_month))

    number_bedrooms_in = MapCompose(to_number_bedrooms)

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    epc_rating_in = MapCompose(to_epc_rating)