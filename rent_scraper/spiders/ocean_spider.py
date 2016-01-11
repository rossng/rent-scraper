import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.ocean_loader import OceanPropertyLoader
from rent_scraper.items import PropertyItem


class OceanSpider(scrapy.Spider):
    name = "ocean"
    allowed_domains = ["oceanhome.co.uk"]
    custom_settings = {'FEED_URI': 'properties_ocean.json'}

    def start_requests(self):
        return [scrapy.FormRequest("http://www.oceanhome.co.uk/search.aspx?ListingType=6&areainformation=0%7C0%7C0%7C%7C28&areainformationname=Clifton&radius=1609.34&bedrooms=&igid=&imgid=9&egid=&emgid=&category=1&defaultlistingtype=5&markettype=0&currency=GBP&statusids=0",
                                   formdata={'__EVENTARGUMENT': 'Page=1&Currency=GBP&ItemsPerPage=1000&OrderByColumnIndex=0&OrderByDirection=0',
                                             '__EVENTTARGET': 'ctl00$ctl11',
                                             'ctl00$cntrlCenterRegion$ctl01$cntrlFilterBar$cntrlItemsPerPage': '10',
                                             'ctl00$cntrlCenterRegion$ctl01$cntrlMappingAjaxHelper$txtPage': '1',
                                             'ctl00$cntrlCenterRegion$ctl01$cntrlMappingAjaxHelper$txtRecordsPerPage': '10',
                                             'ctl00$ctl11': 'ctl00$ctl11|ctl00$ctl11'
                                             },
                                   headers={'Origin': 'http://www.oceanhome.co.uk',
                                            'Accept-Encoding': 'gzip, deflate',
                                            'X-MicrosoftAjax': 'Delta=true',
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
                                            },
                                   method='POST',
                                   callback=self.parse)]

    def parse(self, response):
        for href in response.xpath("//a[contains(text(), 'full details')]/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = OceanPropertyLoader(item=PropertyItem(), response=response)
        l.add_xpath('area',
                    "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_lblFormattedAddress']/text()")
        l.add_xpath('street_name',
                    "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_lblFormattedAddress']/text()")
        # l.add_css('postcode', '.detailHeader > h2::text')
        l.add_xpath('price_per_month',
                    "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_lblFormattedPrice']/text()")
        l.add_value('agent', 'Ocean')
        l.add_xpath('number_bedrooms',
                    "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_lblBedrooms']/text()")
        # TODO: bathrooms
        l.add_xpath('description',
                    "//div[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlFullDescription']//text()")
        l.add_xpath('amenities',
                    "//div[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlFullDescription']//text()")
        l.add_xpath('heating_type',
                    "//div[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlFullDescription']//text()")
        l.add_xpath('epc_rating',
                    "//div[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlFullDescription']//text()")

        l.add_value('url', response.url)
        l.add_value('image_url', response.urljoin(response.xpath(
                "//img[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlGallery_cntrlPhotos_ctl00_imgPhoto']/@src")
                                                  .extract()[0]))

        return l.load_item()
