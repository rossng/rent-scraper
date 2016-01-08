import scrapy
from scrapy.crawler import CrawlerProcess
from rent_scraper.spiders import abode_spider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(abode_spider.AbodeSpider)
process.start()