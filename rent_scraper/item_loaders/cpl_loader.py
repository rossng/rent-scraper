import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join, MapCompose

from rent_scraper.processors.chappell_matthews_processors import ChappellAndMatthewsPriceProcessor
from rent_scraper.processors.common_processors import TextSearch, Concatenate, Get, Split
from rent_scraper.processors.cpl_processors import CityPropertyLetsPriceProcessor, \
    CityPropertyLetsNumberBedroomsProcessor


class CityPropertyLetsPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Compose(Split(','), Get(0), Get(1))
    street_name_in = Compose(Split(','), Get(0), Get(0))

    price_per_month_in = CityPropertyLetsPriceProcessor()

    number_bedrooms_in = MapCompose(CityPropertyLetsNumberBedroomsProcessor())

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')