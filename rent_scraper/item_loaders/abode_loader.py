from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from rent_scraper.processors.abode_processors import FormatPrice

class AbodePropertyLoader(ItemLoader):

    default_output_processor = Identity()

    street_name_in = Identity()
    street_name_out = Identity()

    postcode_in = Identity()
    postcode_out = Identity()

    price_per_person_per_month_in = FormatPrice()