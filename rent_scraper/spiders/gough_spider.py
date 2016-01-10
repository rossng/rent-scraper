# coding=utf-8
import scrapy
import re

from rent_scraper.item_loaders.gough_loader import GoughPropertyLoader
from rent_scraper.items import PropertyItem
from math import ceil
from scrapy.linkextractors import LinkExtractor

def process_value(value):
    m = re.search("window.open\('(.+?)'", value)
    if m:
        return m.group(1)

class GoughSpider(scrapy.Spider):
    name = "ubu_lettings"
    allowed_domains = ["housescape.org.uk"]
    custom_settings = { 'FEED_URI': 'properties_gough.json' }
    start_urls = [
        "http://www.housescape.org.uk/cgi-bin/search.pl?goq1&fo=nr,minbeds=5,maxbeds=5,style=7"
    ]

    def parse(self, response):
        pagination_info = response.css(".fontoveride1::text").extract()[0]
        num_pages = int(ceil(int(pagination_info.split(" ")[4])/12.0)) # there are 12 properties per page

        for i in range(0,num_pages):
            yield scrapy.Request(response.urljoin(response.url) + '&' + str(i+1), callback=self.parse_property_list)

    def parse_property_list(self, response):
        link_extractor = LinkExtractor(restrict_xpaths="//a[.//span[@class='moreinfo']]", canonicalize=False, process_value=process_value)
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = GoughPropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', '.bannertable > tr:first-child > td:first-child b::text')
        l.add_css('street_name', '.bannertable > tr:first-child > td:first-child b::text')
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_xpath('price_per_person_per_month', u"//b[contains(text(), '£')]//text()")
        l.add_value('agent', 'Gough Quarters')
        l.add_value('number_bedrooms', 5)
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