import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.accommodation_unlimited_loader import AccommodationUnlimitedPropertyLoader
from rent_scraper.item_loaders.bristol_property_centre_loader import BristolPropertyCentrePropertyLoader
from rent_scraper.item_loaders.property_concept_loader import PropertyConceptPropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class AccommodationUnlimitedSpider(scrapy.Spider):
    name = "accommodation_unlimited"
    allowed_domains = ["aul.org.uk"]
    custom_settings = { 'FEED_URI': 'properties_accommodation_unlimited.json' }
    start_urls = [
        "http://www.aul.org.uk/listings?os=0&b=0&f=1&rt=99999&fr=m&s=1&lr=5000"
    ]

    def parse(self, response):
        for href in response.xpath("//a[contains(text(), 'More detail')]/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = AccommodationUnlimitedPropertyLoader(item=PropertyItem(), response=response)
        l.add_xpath('area', "//div[@class='row property-detail']//p//text()[5]")
        l.add_xpath('street_name', "//div[@class='row property-detail']//p//text()[5]")
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_xpath('price_per_month', "//div[@class='row property-detail']//p//text()[1]")
        l.add_value('agent', 'Accommodation Unlimited')
        l.add_xpath('number_bedrooms', "//div[@class='row property-detail']//p//text()[2]")
        #l.add_css('number_bathrooms', ".roomIcons .roombaths::text")

        l.add_xpath('description', "//div[@class='row property-detail']//p//text()")
        l.add_xpath('amenities', "//div[@class='row property-detail']//p//text()")
        l.add_xpath('heating_type', "//div[@class='row property-detail']//p//text()")
        #l.add_css('epc_rating', "section.singProp.content p::text")

        #l.add_css('let_agreed', ".propertyPrice h2::text")

        l.add_value('url', response.url)
        maybe_image = response.css("div.large-6.columns.text-center img::attr('src')").extract()
        if maybe_image:
            l.add_value('image_url', response.urljoin(maybe_image[0]))

        return l.load_item()