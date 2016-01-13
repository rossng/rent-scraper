import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.let_with_ease_loader import LetWithEasePropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class LetWithEaseSpider(scrapy.Spider):
    name = "let_with_ease"
    allowed_domains = ["letwithease.com"]
    custom_settings = { 'FEED_URI': 'properties_let_with_ease.json' }
    start_urls = [
        "http://www.letwithease.com/properties.asp?page=1&propind=L&country=&town=&area=&MinPrice=&MaxPrice=&MinBeds=&BedsEqual=&PropType=&Furn=&Avail=&O=Price&Dir=DESC&lat=&lng=&zoom=&searchbymap=&locations=&Cat=STUD"
    ]

    def parse(self, response):
        next_page_links = response.css("div.next a.paginglinkTxt::attr('href')").extract()
        if next_page_links is not None and len(next_page_links) > 0:
            next_page_url = response.urljoin(next_page_links[0])
            yield scrapy.Request(next_page_url, callback=self.parse)

        for href in response.css("div.address a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = LetWithEasePropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', '.address::text')
        l.add_css('street_name', '.address::text')
        l.add_css('postcode', '.address::text')
        l.add_css('price_per_month', '.price::text')
        l.add_value('agent', 'Let With Ease')
        l.add_css('number_bedrooms', ".beds::text")
        # TODO: bathrooms
        l.add_css('description', "div.features ul li::text")
        l.add_css('description', "div.description ::text")
        l.add_css('amenities', "div.features ul li::text")
        l.add_css('amenities', "div.description ::text")
        l.add_css('heating_type', "div.features ul li::text")
        l.add_css('heating_type', "div.description ::text")

        #l.add_xpath('epc_rating', "//ul[@id='propDetStarItemsCont1']//li//text()")

        l.add_css('let_agreed', "div.status::text")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("#largePhoto::attr('src')").extract()[0]))

        return l.load_item()