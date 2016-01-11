import re

import scrapy
from future.backports.misc import ceil

from rent_scraper.item_loaders.cpl_loader import CityPropertyLetsPropertyLoader
from rent_scraper.item_loaders.terry_olpin_loader import TerryOlpinPropertyLoader
from rent_scraper.items import PropertyItem
from rent_scraper.processors.cpl_processors import CityPropertyLetsNumberBedroomsProcessor


class CityPropertyLetsSpider(scrapy.Spider):
    name = "city_property_lets"
    allowed_domains = ["city-property-lets.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_city_property_lets.json' }
    start_urls = [
        "http://www.city-property-lets.co.uk/index.php?page=properties&type=students"
    ]

    def parse(self, response):
        for property in response.xpath("//div[@id='content']//div[@class='lightboxGallery']"):
            l = CityPropertyLetsPropertyLoader(item=PropertyItem(), selector=property,
                                               number_bedrooms=CityPropertyLetsNumberBedroomsProcessor()(property.xpath(".//ul/li[3]/text()").extract()[0]))
            l.add_xpath('area', ".//h1/text()")
            l.add_xpath('street_name', ".//h1/text()")
            # l.add_css('postcode', '.detailHeader > h2::text')
            l.add_xpath('price_per_month', ".//li/b/text()")
            l.add_value('agent', 'City Property Lets')
            l.add_xpath('number_bedrooms', ".//ul/li[3]/text()")
            # TODO: bathrooms
            l.add_xpath('description', ".//p//text()")
            l.add_xpath('amenities', ".//p//text()")
            l.add_xpath('amenities', ".//ul//li//text()")
            l.add_xpath('heating_type', ".//p//text()")
            l.add_xpath('heating_type', ".//ul//li//text()")
            # l.add_xpath('epc_rating', ".//p//text()")

            l.add_value('url', response.url)
            l.add_value('image_url', response.urljoin(property.xpath(".//img/@src").extract()[0]))

            yield l.load_item()