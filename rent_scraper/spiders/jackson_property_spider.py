import scrapy
from future.backports.misc import ceil

from rent_scraper.item_loaders.jackson_property_loader import JacksonPropertyPropertyLoader, to_number_bedrooms
from rent_scraper.items import PropertyItem


class JacksonPropertySpider(scrapy.Spider):
    name = "jackson_property"
    allowed_domains = ["jacksonproperty.co.uk"]
    custom_settings = {'FEED_URI': 'properties_jackson_property.json'}

    def start_requests(self):
        return [scrapy.FormRequest("http://www.jacksonproperty.co.uk/properties/",
                                   formdata={'ddlRentMin': '0.00', 'ddlRoomsMax': '1000', 'ddlRoomMin': '0',
                                             'buttonSearch': ''},
                                   method='POST',
                                   callback=self.parse)]

    def parse(self, response):
        number_pages = int(float(response.xpath("count(//div[@class='pagNumbers'])").extract()[0])) - 1

        for i in range(1, number_pages):
            yield scrapy.FormRequest("http://www.jacksonproperty.co.uk/properties/",
                                     formdata={'ddlRentMin': '0.00', 'ddlRoomsMax': '1000', 'ddlRoomMin': '0',
                                               'buttonSearch': '', 'theCountSearch': str(i)},
                                     method='POST',
                                     callback=self.parse_property_list)

    def parse_property_list(self, response):
        for property_id in response.xpath("//input[@name='theId']/@value").extract():
            yield scrapy.FormRequest("http://www.jacksonproperty.co.uk/properties/", callback=self.parse_property_page,
                                     method='POST', formdata={'theId': property_id})

    def parse_property_page(self, response):
        l = JacksonPropertyPropertyLoader(item=PropertyItem(), response=response,
                                          number_bedrooms=to_number_bedrooms(
                                                  response.xpath("//div[@class='searchHeaderRight']/text()").extract()[
                                                      0]))
        # l.add_xpath('area', "//div[@class='searchHeaderLeft']/text()")
        l.add_xpath('street_name', "//div[@class='searchHeaderLeft']/text()")
        # l.add_css('postcode', '.detailHeader > h2::text')
        l.add_xpath('price_per_month', "//div[@class='searchHeaderRight']/text()")
        l.add_value('agent', 'Jackson Property')
        l.add_xpath('number_bedrooms', "//div[@class='searchHeaderRight']/text()")
        # TODO: bathrooms
        l.add_xpath('description', "//div[@class='propertyDetailInfo']//p//text()")
        l.add_xpath('amenities', "//div[@class='propertyDetailInfo']//p//text()")
        l.add_xpath('heating_type', "//div[@class='propertyDetailInfo']//p//text()")
        l.add_xpath('epc_rating', "//div[@class='propertyDetailInfo']//p//text()")

        l.add_value('url', response.url)
        maybe_image = response.xpath("//div[@class='preview']//img/@src").extract()
        l.add_value('image_url', response.urljoin(maybe_image[0]) if maybe_image else "")

        return l.load_item()
