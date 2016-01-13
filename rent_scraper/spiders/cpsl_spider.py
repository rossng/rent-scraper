import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.cpsl_loader import CliftonPropertyServicesPropertyLoader
from rent_scraper.item_loaders.ocean_loader import OceanPropertyLoader
from rent_scraper.items import PropertyItem


class CliftonPropertyServicesSpider(scrapy.Spider):
    name = "clifton_property_services"
    allowed_domains = ["vebra.com"]
    custom_settings = {'FEED_URI': 'properties_clifton_property_services.json'}

    def start_requests(self):
        return [scrapy.FormRequest("http://www.vebra.com/cpsl/property/search",
                                   formdata={'action': 'search',
                                             'bed': '0',
                                             'dbtype': '2',
                                             'hip': '2500',
                                             'key': 'cpsl',
                                             'p': '2',
                                             'lop': '0'
                                             },
                                   headers={'Origin': 'http://www.cpsl.uk.com',
                                            'Accept-Encoding': 'gzip, deflate',
                                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                            'Referer': 'http://www.cpsl.uk.com/',
                                            'Content-Type': 'application/x-www-form-urlencoded',
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
                                            },
                                   method='POST',
                                   callback=self.parse)]

    def parse(self, response):
        num_pages = int(response.css("div#s-pagenavtop > p:first-child::text").extract()[0].split(' ')[-1])
        for i in range(1, num_pages+1):
            yield scrapy.Request("http://www.vebra.com/cpsl/property/search/results/2/" + str(i), callback=self.parse_property_list)

    def parse_property_list(self, response):
        for url in response.css("li.rsbldetails a::attr('href')").extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = CliftonPropertyServicesPropertyLoader(item=PropertyItem(), response=response)
        l.add_xpath('area', "//h3[@class='fulladdress']/text()")
        l.add_xpath('street_name', "//h3[@class='fulladdress']/text()")
        # l.add_css('postcode', '.detailHeader > h2::text')
        l.add_xpath('price_per_month', "//h2[@class='dtaddress']/em/text()")
        l.add_value('agent', 'Clifton Property Services')
        l.add_xpath('number_bedrooms', "//span[@class='rs-bedrooms']/text()")
        # TODO: bathrooms
        l.add_xpath('description', "//div[@id='s-dtintrodesc']//text()")
        l.add_xpath('description', "//ul[@id='s-dtbullets']//text()")
        l.add_xpath('amenities', "//div[@id='s-dtintrodesc']//text()")
        l.add_xpath('amenities', "//ul[@id='s-dtbullets']//text()")
        l.add_xpath('heating_type', "//div[@id='s-dtintrodesc']//text()")
        l.add_xpath('heating_type', "//ul[@id='s-dtbullets']//text()")
        #l.add_xpath('epc_rating',"//div[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlFullDescription']//text()")
        l.add_xpath('let_agreed', "h2[@class='dtaddress']/em/span[@class='PropStatus']/text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.xpath("//img[@id='mainimage']/@src").extract()[0]))

        return l.load_item()
