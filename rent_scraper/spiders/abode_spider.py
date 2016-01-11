import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.items import PropertyItem


class AbodeSpider(scrapy.Spider):
    name = "abode"
    allowed_domains = ["yourabode.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_abode.json' }
    start_urls = [
        "http://yourabode.co.uk/modules/letting/searchresults.php?sector=Student&area[]=Brentry&area[]=City+Centre&area[]=Clifton&area[]=Cotham&area[]=Horfield&area[]=Kingsdown&area[]=Montpellier&area[]=Redland&area[]=Sneyd+Park&area[]=Stoke+Bishop&area[]=Westbury+Park&professionalprice_range[]=1&professionalprice_range[]=2&professionalprice_range[]=3&professionalprice_range[]=4&professionalbedrooms[]=0&professionalbedrooms[]=1&professionalbedrooms[]=2&professionalbedrooms[]=3&professionalbedrooms[]=4&studentbedrooms[]=5&furnished[]=0&furnished[]=2&furnished[]=1&ajax=true&action=search"
    ]

    def parse(self, response):
        for href in response.css(".listingWrap p.more > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = AbodePropertyLoader(item=PropertyItem(), response=response, number_bedrooms=5)
        l.add_css('area', '.detailHeader > h2::text')
        l.add_css('street_name', '.detailHeader > h2::text')
        l.add_css('postcode', '.detailHeader > h2::text')
        l.add_css('price_per_month', '.detailHeader > h2 > strong::text')
        l.add_value('agent', 'Abode')
        l.add_value('number_bedrooms', 5)
        # TODO: bathrooms
        l.add_xpath('description', "//div[@id='description']/div[@class='inner']//text()")
        l.add_xpath('amenities', "//div[@id='description']/div[@class='inner']//text()")
        l.add_xpath('amenities', "//div[@class='features']//li//text()")
        l.add_xpath('heating_type', "//div[@id='description']/div[@class='inner']//text()")
        l.add_xpath('heating_type', "//div[@class='features']//li//text()")
        l.add_xpath('epc_rating', "//div[@class='features']//li//text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("#mainImg > img::attr('src')").extract()[0]))

        return l.load_item()