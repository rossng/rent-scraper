import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class UbuLettingsSpider(scrapy.Spider):
    name = "ubu_lettings"
    allowed_domains = ["expertagent.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_ubu.json' }
    start_urls = [
        "http://powering2.expertagent.co.uk/customsearch.aspx?aid={7168595e-e672-4cea-9645-f911650e6f5c}&DefaultPage=3&dep=2&radius=5&minbeds=5&maxbeds=5&minprice=&maxprice="
    ]

    def parse(self, response):
        next_page_links = response.css("#propListPrevNextCont td.col2 > a::attr('href')").extract()
        if next_page_links is not None and len(next_page_links) > 0:
            next_page_url = response.urljoin(next_page_links[0])
            yield scrapy.Request(next_page_url, callback=self.parse)

        for href in response.css(".propListItemCont .propListItemTemplateDescription > a#moreDetails::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = UbuLettingsPropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', '#propAddress::text')
        l.add_css('street_name', '#propAddress::text')
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_css('price_per_month', '#propPrice::text')
        l.add_value('agent', 'UBU Lettings')
        l.add_value('number_bedrooms', 5)
        # TODO: bathrooms
        l.add_xpath('description', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('description', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('amenities', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('amenities', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('heating_type', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('heating_type', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('epc_rating', "//ul[@id='propDetStarItemsCont1']//li//text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.css("#mainImage::attr('src')").extract()[0]))

        return l.load_item()