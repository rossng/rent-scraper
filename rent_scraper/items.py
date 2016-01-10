import scrapy


class RentScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PropertyItem(scrapy.Item):
    url = scrapy.Field()
    image_url = scrapy.Field()
    area = scrapy.Field()
    street_name = scrapy.Field()
    postcode = scrapy.Field()
    agent = scrapy.Field()
    price_per_person_per_month = scrapy.Field()
    number_bedrooms = scrapy.Field()
    number_bathrooms = scrapy.Field()
    description = scrapy.Field()
    amenities = scrapy.Field()
    heating_type = scrapy.Field()
    epc_rating = scrapy.Field()
    let_agreed = scrapy.Field()