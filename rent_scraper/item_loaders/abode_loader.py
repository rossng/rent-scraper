from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join
from rent_scraper.processors.abode_processors import \
    AbodePriceProcessor, AbodePostcodeProcessor, AbodeAreaProcessor, AbodeStreetProcessor, AbodeEpcRatingProcessor
from rent_scraper.processors.common_processors import TextSearch


class AbodePropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = AbodeAreaProcessor()

    street_name_in = AbodeStreetProcessor()

    postcode_in = AbodePostcodeProcessor()

    price_per_person_per_month_in = AbodePriceProcessor()

    description_out = Join()

    has_washing_machine_in = TextSearch('washing machine')

    has_parking_in = TextSearch('parking')

    has_dishwasher_in = TextSearch('dishwasher')

    heating_type_in = Compose(lambda is_gas: 'gas' if is_gas else 'unknown', TextSearch('gas'))

    epc_rating_in = AbodeEpcRatingProcessor()