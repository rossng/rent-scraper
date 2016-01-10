import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.absolute_loader import AbsolutePropertyLoader
from rent_scraper.items import PropertyItem


class AbsoluteSpider(scrapy.Spider):
    name = "absolute"
    allowed_domains = ["absoluteproperty.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_absolute.json' }

    def start_requests(self):
        return [scrapy.FormRequest("http://www.absoluteproperty.co.uk/search-results",
                                   formdata={'area': '0', 'bedrooms': '5', 'type': '4', 'submit': 'Search'},
                                   callback=self.parse)]

    def parse(self, response):
        for href in response.css("article.absolute_property a.more-details-link::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = AbsolutePropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', '.property-area::text')
        l.add_css('street_name', 'h3.property-address::text')
        l.add_css('postcode', 'h3.property-address::text')
        l.add_css('price_per_person_per_month', '.property-price::text')
        l.add_value('agent', 'Absolute Property')
        l.add_css('number_bedrooms', '.property-bedrooms::text')
        l.add_css('let_agreed', '.property-status::text')
        l.add_css('description', '.property-description')
        l.add_css('amenities', '.property-description')
        l.add_css('heating_type', '.property-description')

        # TODO: bathrooms, epc rating

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("img.attachment-full::attr('src')").extract()[0]))

        return l.load_item()