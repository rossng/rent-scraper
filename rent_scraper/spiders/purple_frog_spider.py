import scrapy

from rent_scraper.item_loaders.purple_frog_loader import to_number_bedrooms, PurpleFrogPropertyLoader
from rent_scraper.items import PropertyItem


class PurpleFrogSpider(scrapy.Spider):
    name = "purple_frog"
    allowed_domains = ["purplefrogproperty.com"]
    custom_settings = { 'FEED_URI': 'properties_purple_frog.json' }
    start_urls = [
        "http://www.purplefrogproperty.com/student-accommodation/Bristol/?beds=&year=next&type=&price[from]=0&price[to]=185&view=list"
    ]

    def parse(self, response):
        next_page_links = response.css(".pagination-links li.next.page a::attr('href')").extract()
        if next_page_links is not None and len(next_page_links) > 0:
            next_page_url = response.urljoin(next_page_links[0])
            yield scrapy.Request(next_page_url, callback=self.parse)

        for href in response.css("div.property-info h2 a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        number_bedrooms = to_number_bedrooms(response.css("li.beds span::text").extract()[0])
        l = PurpleFrogPropertyLoader(item=PropertyItem(), response=response, number_bedrooms=number_bedrooms)
        l.add_css('area', "h1.property-title::text")
        l.add_css('street_name', "h1.property-title::text")
        l.add_css('postcode', "h1.property-title::text")
        l.add_css('price_per_month', "div.prices span.price::text")
        l.add_value('agent', 'Purple Frog')
        l.add_css('number_bedrooms', "li.beds span::text")
        #l.add_css('number_bathrooms', "ul.icons li.baths span::text")

        l.add_css('description', "div#description div.left-content-panel p::text")
        l.add_css('amenities', "div#description div.left-content-panel p::text")
        l.add_css('amenities', "div.features i::text")
        l.add_css('heating_type', "div#description div.left-content-panel p::text")
        l.add_css('heating_type', "div.features i::text")
        l.add_css('epc_rating', ".indicators .indicator.ind-current span::text")

        #l.add_css('let_agreed', "span.soldbar::text")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css(".main-img img::attr('src')").extract()[0]))

        return l.load_item()