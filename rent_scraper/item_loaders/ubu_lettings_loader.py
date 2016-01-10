from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose, Join

from rent_scraper.processors.common_processors import TextSearch, Concatenate
from rent_scraper.processors.ubu_lettings_processors import UbuLettingsAreaProcessor, UbuLettingsEpcRatingProcessor, \
UbuLettingsEpcRatingProcessor, UbuLettingsPostcodeProcessor, UbuLettingsPriceProcessor, UbuLettingsStreetProcessor

class UbuLettingsPropertyLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    area_in = UbuLettingsAreaProcessor()

    street_name_in = UbuLettingsStreetProcessor()

    postcode_in = UbuLettingsPostcodeProcessor()

    price_per_person_per_month_in = UbuLettingsPriceProcessor()

    description_out = Join()

    amenities_in = Concatenate(
            Compose(TextSearch('washing machine'), lambda x: ['Washing machine'] if x else []),
            Compose(TextSearch('parking'), lambda x: ['Parking'] if x else []),
            Compose(TextSearch('dishwasher'), lambda x: ['Dishwasher'] if x else [])
    )
    amenities_out = Identity()

    heating_type_in = Compose(TextSearch('gas'), lambda is_gas: 'gas' if is_gas else 'unknown')

    epc_rating_in = UbuLettingsEpcRatingProcessor()