from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join
from rent_scraper.processors.abode_processors import \
    AbodePriceProcessor, AbodePostcodeProcessor, AbodeAreaProcessor, AbodeStreetProcessor, AbodeEpcRatingProcessor
from rent_scraper.processors.common_processors import TextSearch, Concatenate


class AbodePropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = AbodeAreaProcessor()

    street_name_in = AbodeStreetProcessor()

    postcode_in = AbodePostcodeProcessor()

    price_per_person_per_month_in = AbodePriceProcessor()

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    epc_rating_in = AbodeEpcRatingProcessor()