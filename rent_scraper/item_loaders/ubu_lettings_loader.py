from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join

from rent_scraper.processors.common_processors import TextSearch, Concatenate, Split, Get
from rent_scraper.processors.ubu_lettings_processors import UbuLettingsEpcRatingProcessor, UbuLettingsPriceProcessor

class UbuLettingsPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = Compose(Split(','), Get(0), Get(1))

    street_name_in = Compose(Split(','), Get(0), Get(0))

    postcode_in = Compose(Split(','), Get(0), Get(2))

    price_per_month_in = UbuLettingsPriceProcessor()

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    epc_rating_in = UbuLettingsEpcRatingProcessor()