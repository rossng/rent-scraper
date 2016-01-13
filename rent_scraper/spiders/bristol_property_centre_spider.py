import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.bristol_property_centre_loader import BristolPropertyCentrePropertyLoader
from rent_scraper.item_loaders.property_concept_loader import PropertyConceptPropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class BristolPropertyCentreSpider(scrapy.Spider):
    name = "bristol_property_centre"
    allowed_domains = ["bristolpropertycentre.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_bristol_property_centre.json' }
    start_urls = [
        "http://www.bristolpropertycentre.co.uk/search/?showstc=on&showsold=on&instruction_type=Letting&address_keyword=&minprice=&maxprice=&bedrooms=1&showstc=on&showsold=on&n=1000"
    ]

    def parse(self, response):
        for href in response.css(".resultsDetails h2 a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = BristolPropertyCentrePropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', "#propertyContent h1::text")
        l.add_css('street_name', "#propertyContent h1::text")
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_css('price_per_month', ".propertyPrice h2::text")
        l.add_value('agent', 'Bristol Property Centre')
        l.add_css('number_bedrooms', ".roomIcons .roombeds::text")
        l.add_css('number_bathrooms', ".roomIcons .roombaths::text")

        l.add_css('description', "#propertyDescription p ::text")
        l.add_css('description', "#keyFeatures ul li ::text")
        l.add_css('amenities', "#propertyDescription p ::text")
        l.add_css('amenities', "#keyFeatures ul li ::text")
        l.add_css('heating_type', "#propertyDescription p ::text")
        l.add_css('heating_type', "#keyFeatures ul li ::text")
        #l.add_css('epc_rating', "section.singProp.content p::text")

        l.add_css('let_agreed', ".propertyPrice h2::text")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("meta[property='og:image']::attr('content')").extract()[0]))

        return l.load_item()