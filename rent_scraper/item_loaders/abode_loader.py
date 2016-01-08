from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose
from rent_scraper.processors.abode_processors import AbodePriceProcessor, AbodePostcodeProcessor, AbodeAreaProcessor, AbodeStreetProcessor

class AbodePropertyLoader(ItemLoader):

    default_output_processor = Identity()

    agent_in = Identity()
    agent_out = TakeFirst()

    area_in = AbodeAreaProcessor()
    area_out = TakeFirst()

    street_name_in = AbodeStreetProcessor()
    street_name_out = TakeFirst()

    postcode_in = AbodePostcodeProcessor()
    postcode_out = TakeFirst()

    price_per_person_per_month_in = AbodePriceProcessor()
    price_per_person_per_month_out = TakeFirst()

    number_bedrooms_in = Identity()
    number_bedrooms_out = TakeFirst()

    description_in = Identity()
    description_out = Identity()