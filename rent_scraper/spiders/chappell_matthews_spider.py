import scrapy
from future.backports.misc import ceil

from rent_scraper.item_loaders.chappell_matthews_loader import ChappellAndMatthewsPropertyLoader
from rent_scraper.items import PropertyItem


class ChappellAndMatthewsSpider(scrapy.Spider):
    name = "chappell_and_matthews"
    allowed_domains = ["chappellandmatthews.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_chappell_and_matthews.json' }
    start_urls = [
        "http://www.chappellandmatthews.co.uk/rent/search/bs8 1lt/within-1-miles/p-studentfriendly/"
    ]

    def parse(self, response):
        next_page_links = response.xpath("//a[@class='pagingbutton' and @title='Next']/@href").extract()
        if next_page_links:
            next_page_url = response.urljoin(next_page_links[0])
            yield scrapy.Request(next_page_url, callback=self.parse)

        for href in response.xpath("//ul[@id='ResultsList']/li//a[@title='Read More']/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = ChappellAndMatthewsPropertyLoader(item=PropertyItem(), response=response)
        l.add_xpath('area', "//div[@id='DetailsPriceAndContactContainer']//h1/text()")
        l.add_xpath('street_name', "//h2[@class='DescriptionAddress']/text()")
        l.add_xpath('postcode', "//h2[@class='DescriptionAddress']/text()")
        l.add_xpath('price_per_month', "//label[@class='generic-price']/text()")
        l.add_value('agent', 'Chappell And Matthews')
        l.add_xpath('number_bedrooms', "//li[@class='Bedrooms']//h2/text()")
        # TODO: bathrooms, epc rating
        l.add_xpath('description', "//div[@id='DetailsContentContainer']//text()")
        l.add_xpath('amenities', "//div[@id='DetailsContentContainer']//text()")
        l.add_xpath('heating_type', "//div[@id='DetailsContentContainer']//text()")
        l.add_xpath('let_agreed', "//div[@id='GlobalPropertyDetails']//div[@class='LetAgreed']/text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.xpath("//img[@id='imgMainPhoto']/@src").extract()[0]))

        yield l.load_item()