import scrapy
from future.backports.misc import ceil

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.kingsley_thomas_loader import KingsleyThomasPropertyLoader
from rent_scraper.items import PropertyItem


class KingsleyThomasSpider(scrapy.Spider):
    name = "kingsley_thomas"
    allowed_domains = ["kingsleythomas.co.uk"]
    custom_settings = { 'FEED_URI': 'properties_kingsley_thomas.json' }
    start_urls = [
        "http://www.kingsleythomas.co.uk/list.asp?chk_student=Student&chkarea=All+Areas&chkarea=Bradley+Stoke&chkarea=Clifton&chkarea=Horfield&chkarea=Kingsdown&chkarea=St+Andrews&chkarea=Bishopston&chkarea=Brentry&chkarea=Cotham&chkarea=Hotwells&chkarea=Redland&txt_min_rent=&txt_max_rent=&button=Search+now"
    ]

    def parse(self, response):
        pagination_info = response.xpath("//span[@class='bodytextbold' and contains(text(),'Your search produced')]//text()").extract()[0]
        num_properties = int(pagination_info.split(" ")[3])

        for i in range(0, num_properties, 5):
            yield scrapy.Request(response.urljoin(response.url) + '&offset=' + str(i), callback=self.parse_property_list)

    def parse_property_list(self, response):
        for property in response.xpath("//table[@width='96%']"):
            l = KingsleyThomasPropertyLoader(item=PropertyItem(), selector=property)
            l.add_xpath('area', ".//td[@width='31%']/text()")
            #l.add_css('street_name', '.detailHeader > h2::text')
            #l.add_css('postcode', '.detailHeader > h2::text')
            l.add_xpath('price_per_month', ".//td[@width='20%']/text()")
            l.add_value('agent', 'Kingsley Thomas')
            l.add_xpath('number_bedrooms', ".//td[@width='17%']/text()")
            # TODO: bathrooms
            l.add_xpath('description', ".//p//text()")
            l.add_xpath('amenities', ".//p//text()")
            l.add_xpath('heating_type', ".//p//text()")
            l.add_xpath('epc_rating', ".//p//text()")

            l.add_value('url', response.url)
            l.add_value('image_url', response.urljoin(property.xpath(".//img/@src").extract()[0]))

            yield l.load_item()