import scrapy
from future.backports.misc import ceil

from rent_scraper.item_loaders.terry_olpin_loader import TerryOlpinPropertyLoader
from rent_scraper.items import PropertyItem


class TerryOlpinSpider(scrapy.Spider):
    name = "terry_olpin"
    allowed_domains = ["olpin.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_terry_olpin.json' }
    start_urls = [
        "http://olpin.co.uk/list.asp?chk_student=Student&chkarea=All+Areas&chkarea=Bristol&chkarea=Central+Bristol&chkarea=Clifton+Village&chkarea=Entrance+on+Hill+St&chkarea=Queen+Charlotte+Street&chkarea=Redland&chkarea=Westbury+Park&chkarea=Bishopston&chkarea=CLIFTON&chkarea=Clifton&chkarea=Cotham&chkarea=Off+Park+St&chkarea=Rear+of+Park+St&chkarea=St+Andrews&select_rooms=Any&txt_min_rent=&txt_max_rent=&button=Search+now"
    ]

    def parse(self, response):
        pagination_info = response.xpath("//span[@class='bodytextbold' and contains(text(),'Your search produced')]//text()").extract()[0]
        num_properties = int(pagination_info.split(" ")[3])

        for i in range(0, num_properties, 5):
            yield scrapy.Request(response.urljoin(response.url) + '&offset=' + str(i), callback=self.parse_property_list)

    def parse_property_list(self, response):
        for property in response.xpath("//table[@width='96%']"):
            l = TerryOlpinPropertyLoader(item=PropertyItem(), selector=property)
            l.add_xpath('area', ".//td[@width='31%']/text()")
            #l.add_css('street_name', '.detailHeader > h2::text')
            #l.add_css('postcode', '.detailHeader > h2::text')
            l.add_xpath('price_per_month', ".//td[@width='20%']/text()")
            l.add_value('agent', 'Terry Olpin')
            l.add_xpath('number_bedrooms', ".//td[@width='17%']/text()")
            # TODO: bathrooms
            l.add_xpath('description', ".//p//text()")
            l.add_xpath('amenities', ".//p//text()")
            l.add_xpath('heating_type', ".//p//text()")
            l.add_xpath('epc_rating', ".//p//text()")

            l.add_value('url', response.url)
            l.add_value('image_url', response.urljoin(property.xpath(".//img/@src").extract()[0]))

            yield l.load_item()