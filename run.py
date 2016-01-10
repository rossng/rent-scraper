import os
from glob import glob

from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

from rent_scraper.spiders.abode_spider import AbodeSpider
from rent_scraper.spiders.gough_spider import GoughSpider
from rent_scraper.spiders.tlg_spider import TheLettingGameSpider
from rent_scraper.spiders.ubu_lettings_spider import UbuLettingsSpider
from rent_scraper.spiders.absolute_spider import AbsoluteSpider

for file in glob('properties_*.json'):
    os.remove(file)

settings = get_project_settings()

process = CrawlerProcess(get_project_settings())

process.crawl(AbodeSpider)
process.crawl(UbuLettingsSpider)
process.crawl(AbsoluteSpider)
process.crawl(GoughSpider)
process.crawl(TheLettingGameSpider)
process.start()