import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.property_concept_loader import PropertyConceptPropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class PropertyConceptSpider(scrapy.Spider):
    name = "property_concept"
    allowed_domains = ["propertyconcept.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_property_concept.json' }
    start_urls = [
        "http://www.propertyconcept.co.uk/search-rental/?minprice=0&maxprice=99999999"
    ]

    def parse(self, response):
        next_page_links = response.css(".pagination > a.next.page-numbers::attr('href')").extract()
        if next_page_links is not None and len(next_page_links) > 0:
            next_page_url = response.urljoin(next_page_links[0])
            yield scrapy.Request(next_page_url, callback=self.parse)

        for href in response.css(".pContent a.rMore::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = PropertyConceptPropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', "div.introBox h1::text")
        l.add_css('street_name', "div.introBox h1::text")
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_css('price_per_month', "div.introBox p.pPrice::text")
        l.add_value('agent', 'Property Concept')
        l.add_css('number_bedrooms', "ul.icons li.beds span::text")
        l.add_css('number_bathrooms', "ul.icons li.baths span::text")

        l.add_css('description', "section.singProp.content p::text")
        l.add_css('description', "div.left ul li::text")
        l.add_css('amenities', "section.singProp.content p::text")
        l.add_css('amenities', "div.left ul li::text")
        l.add_css('heating_type', "section.singProp.content p::text")
        l.add_css('heating_type', "div.left ul li::text")
        l.add_css('epc_rating', "section.singProp.content p::text")

        l.add_css('let_agreed', "span.soldbar::text")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("#slider img::attr('src')").extract()[0]))

        return l.load_item()