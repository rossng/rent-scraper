import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join, MapCompose

from rent_scraper.processors.common_processors import TextSearch, Concatenate, Get, Split
from rent_scraper.processors.kingsley_thomas_processors import KingsleyThomasPriceProcessor


def get_bedrooms(text):
    match_or_none = re.search("(\d+) rooms", text, re.IGNORECASE)
    return int(match_or_none.group(1)) if match_or_none else None


def get_epc_rating(text):
    match_or_none = re.search("EPC Rating \d\d \((.)\)", text, re.IGNORECASE)
    return match_or_none.group(1) if match_or_none else None


class KingsleyThomasPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Identity()

    price_per_month_in = KingsleyThomasPriceProcessor()

    number_bedrooms_in = MapCompose(get_bedrooms)

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    epc_rating_in = MapCompose(get_epc_rating)