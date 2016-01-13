import scrapy
from future.backports.misc import ceil

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.property_concept_loader import PropertyConceptPropertyLoader
from rent_scraper.item_loaders.sure_move_loader import SureMovePropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class SureMoveSpider(scrapy.Spider):
    name = "sure_move"
    allowed_domains = ["suremovebristol.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_sure_move.json' }
    start_urls = [
        "http://www.suremovebristol.co.uk/properties/residential_lettings/list?lettings_furnished_ids=0,4"
    ]

    def parse(self, response):
        pagination_info = response.css("div.property-number p::text").extract()[0]
        number_pages = int(ceil(int(pagination_info)/5.0))

        for i in range(0, number_pages):
            yield scrapy.Request(response.urljoin(response.url) + '&page=' + str(i+1), callback=self.parse_property_list)

    def parse_property_list(self, response):
        for href in response.css(".view-buttons a.more::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = SureMovePropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', "p.address::text")
        l.add_css('street_name', "p.address::text")
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_css('price_per_month', "span.property-price::text")
        l.add_value('agent', 'Sure Move')
        l.add_css('number_bedrooms', "ul.guide li.beds::text")
        l.add_css('number_bathrooms', "ul.guide li.bath::text")

        l.add_css('description', ".property-description p ::text")
        l.add_css('amenities', ".property-description p ::text")
        l.add_css('heating_type', ".property-description p ::text")
        #l.add_css('epc_rating', "section.singProp.content p::text")

        l.add_css('let_agreed', "div.banner-agreed p::text")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("img.main-prop-image::attr('src')").extract()[0]))

        return l.load_item()