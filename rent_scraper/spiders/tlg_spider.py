import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.tlg_loader import TheLettingGamePropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class TheLettingGameSpider(scrapy.Spider):
    name = "the_letting_game"
    allowed_domains = ["thelettinggame.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_tlg.json' }
    start_urls = [
        "http://www.thelettinggame.co.uk/search/?showstc=on&showsold=on&instruction_type=Letting&address_keyword=&bedrooms=&minprice=&maxprice="
    ]

    def parse(self, response):
        next_page_links = response.xpath("//a[@rel='next']/@href").extract()
        if next_page_links:
            next_page_url = response.urljoin(next_page_links[0])
            yield scrapy.Request(next_page_url, callback=self.parse)

        for href in response.css(".resultsDetails h2 a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = TheLettingGamePropertyLoader(item=PropertyItem(), response=response)
        l.add_xpath('area', "//div[@id='propertyAddress']//span[@itemprop='name']/text()")
        l.add_xpath('street_name', "//div[@id='propertyAddress']//span[@itemprop='name']/text()")
        l.add_xpath('postcode', "//div[@id='propertyAddress']//span[@itemprop='name']/text()")

        l.add_xpath('price_per_month', "//div[@id='propertyAddress']//span[@itemprop='price']/text()")
        l.add_value('agent', 'The Letting Game')

        l.add_css('number_bedrooms', "li.bedrooms::text")
        # TODO: bathrooms, epc
        l.add_xpath('description', "//p[@itemprop='description']//text()")
        l.add_xpath('amenities', "//p[@itemprop='description']//text()")
        l.add_xpath('amenities', "//ul[@class='result-bullets']//li//text()")
        l.add_xpath('heating_type', "//p[@itemprop='description']//text()")
        l.add_xpath('heating_type', "//ul[@class='result-bullets']//li//text()")
        #l.add_xpath('epc_rating', "//ul[@id='propDetStarItemsCont1']//li//text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css(".carousel-inner img::attr('src')").extract()[0]))

        return l.load_item()