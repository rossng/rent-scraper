# coding=utf-8
import scrapy
import re

from rent_scraper.item_loaders.berkeley_estates_loader import BerkeleyEstatesPropertyLoader, to_number_bedrooms
from rent_scraper.item_loaders.gough_loader import GoughPropertyLoader
from rent_scraper.items import PropertyItem
from math import ceil
from scrapy.linkextractors import LinkExtractor

def process_value(value):
    m = re.search("window.open\('(.+?)'", value)
    if m:
        return m.group(1)

class BerkeleyEstatesSpider(scrapy.Spider):
    name = "berkeley_estates"
    allowed_domains = ["housescape.org.uk"]
    custom_settings = { 'FEED_URI': 'properties_berkeley_estates.json' }
    start_urls = [
        "http://www2.housescape.org.uk/cgi-bin/search.pl?chg1&style=20,configfile=2,fo=r,mp=9999&1&keywords=bristol"
    ]

    def parse(self, response):
        link_extractor = LinkExtractor(restrict_xpaths="//div[@class='main-image']//a[.//img]", canonicalize=False, process_value=process_value)
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = BerkeleyEstatesPropertyLoader(item=PropertyItem(), response=response, number_bedrooms=to_number_bedrooms(
                response.xpath("//table[@class='bannertable']//tr[1]//td[2]//b/text()").extract()[0]))
        l.add_css('area', '.bannertable > tr:first-child > td:first-child b::text')
        l.add_css('street_name', '.bannertable > tr:first-child > td:first-child b::text')
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_xpath('price_per_month', u"//b[contains(text(), '£')]//text()")
        l.add_value('agent', 'Berkeley Estates')
        l.add_xpath('number_bedrooms', "//table[@class='bannertable']//tr[1]//td[2]//b/text()")
        l.add_xpath('number_bathrooms', "//table[@class='bannertable']//tr[1]//td[2]//b/text()")
        # TODO: bathrooms, epc
        l.add_xpath('description', "//td[.//*[contains(text(),'Full Description')]]//text()")
        l.add_xpath('description', "//ul//text()")
        l.add_xpath('amenities', "//td[.//*[contains(text(),'Full Description')]]//text()")
        l.add_xpath('amenities', "//ul//text()")
        l.add_xpath('heating_type', "//td[.//*[contains(text(),'Full Description')]]//text()")
        l.add_xpath('heating_type', "//ul//text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css(".image img::attr('src')").extract()[0]))

        return l.load_item()