from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

from rent_scraper.spiders.abode_spider import AbodeSpider
from rent_scraper.spiders.ubu_lettings_spider import UbuLettingsSpider

settings = get_project_settings()

process = CrawlerProcess(get_project_settings())

process.crawl(AbodeSpider)
process.crawl(UbuLettingsSpider)
process.start()