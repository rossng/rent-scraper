import os
from glob import glob

from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

from rent_scraper.spiders.abode_spider import AbodeSpider
from rent_scraper.spiders.ubu_lettings_spider import UbuLettingsSpider

for file in glob('properties_*.json'):
    os.remove(file)

settings = get_project_settings()

process = CrawlerProcess(get_project_settings())

abode_spider = AbodeSpider()
#abode_spider.settings['FEED_URI'] = 'properties_abode.json'

ubu_spider = UbuLettingsSpider()
#ubu_spider.settings['FEED_URI'] = 'properties_ubu.json'

process.crawl(abode_spider)
process.crawl(ubu_spider)
process.start()