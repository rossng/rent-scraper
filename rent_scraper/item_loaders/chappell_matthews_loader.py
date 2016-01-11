import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join, MapCompose

from rent_scraper.processors.chappell_matthews_processors import ChappellAndMatthewsPriceProcessor
from rent_scraper.processors.common_processors import TextSearch, Concatenate, Get, Split


def get_epc_rating(text):
    match_or_none = re.search("EPC Rating \d\d \((.)\)", text, re.IGNORECASE)
    return match_or_none.group(1) if match_or_none else None


class ChappellAndMatthewsPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Compose(Split(','), Get(0), Get(0))
    street_name_in = Compose(Split(','), Get(0), Get(1))
    postcode_in = Compose(Split(','), Get(0), Get(-1))

    price_per_month_in = ChappellAndMatthewsPriceProcessor()

    number_bedrooms_in = Compose(Split(' '), Get(0), Get(0))

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')