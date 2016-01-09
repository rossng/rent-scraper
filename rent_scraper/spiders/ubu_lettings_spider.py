import scrapy

from rent_scraper.item_loaders.abode_loader import AbodePropertyLoader
from rent_scraper.item_loaders.ubu_lettings_loader import UbuLettingsPropertyLoader
from rent_scraper.items import PropertyItem


class UbuLettingsSpider(scrapy.Spider):
    name = "ubu_lettings"
    allowed_domains = ["expertagent.co.uk"]
    start_urls = [
        "http://powering2.expertagent.co.uk/customsearch.aspx?aid={7168595e-e672-4cea-9645-f911650e6f5c}&DefaultPage=3&dep=2&radius=5&minbeds=5&minprice=&maxprice="
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        for href in response.css(".propListItemCont .propListItemTemplateDescription > a#moreDetails::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_property_page)

    def parse_property_page(self, response):
        l = UbuLettingsPropertyLoader(item=PropertyItem(), response=response)
        l.add_css('area', '#propAddress::text')
        l.add_css('street_name', '#propAddress::text')
        #l.add_css('postcode', '.detailHeader > h2::text')
        l.add_css('price_per_person_per_month', '#propPrice::text')
        l.add_value('agent', 'UBU Lettings')
        l.add_value('number_bedrooms', 5)
        # TODO: bathrooms
        l.add_xpath('description', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('description', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('has_washing_machine', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('has_washing_machine', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('has_parking', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('has_parking', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('has_dishwasher', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('has_dishwasher', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('heating_type', "//div[@id='propDetShortDescCont1']//text()")
        l.add_xpath('heating_type', "//ul[@id='propDetStarItemsCont1']//li//text()")
        l.add_xpath('epc_rating', "//ul[@id='propDetStarItemsCont1']//li//text()")

        l.add_value('url', response.url)
        return l.load_item()