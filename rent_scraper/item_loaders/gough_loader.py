from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join

from rent_scraper.processors.common_processors import TextSearch, Concatenate, Split, Get
from rent_scraper.processors.gough_processor import GoughPriceProcessor


class GoughPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Compose(Split(' - '), Get(0), Get(1))

    street_name_in = Compose(Split(' - '), Get(0), Get(1))

    postcode_in = Identity()

    price_per_month_in = GoughPriceProcessor()

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    let_agreed_in = Compose(lambda xs: 'Yes' if any('Let' in x for x in xs) else 'No')