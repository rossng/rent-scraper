import os
from glob import glob

from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

from rent_scraper.spiders.abode_spider import AbodeSpider
from rent_scraper.spiders.accommodation_unlimited_spider import AccommodationUnlimitedSpider
from rent_scraper.spiders.bristol_property_centre_spider import BristolPropertyCentreSpider
from rent_scraper.spiders.chappell_matthews_spider import ChappellAndMatthewsSpider
from rent_scraper.spiders.cpl_spider import CityPropertyLetsSpider
from rent_scraper.spiders.cpsl_spider import CliftonPropertyServicesSpider
from rent_scraper.spiders.flatline_spider import FlatlineSpider
from rent_scraper.spiders.gough_spider import GoughSpider
from rent_scraper.spiders.jackson_property_spider import JacksonPropertySpider
from rent_scraper.spiders.kingsley_thomas_spider import KingsleyThomasSpider
from rent_scraper.spiders.ocean_spider import OceanSpider
from rent_scraper.spiders.property_concept_spider import PropertyConceptSpider
from rent_scraper.spiders.purple_frog_spider import PurpleFrogSpider
from rent_scraper.spiders.sure_move_spider import SureMoveSpider
from rent_scraper.spiders.terry_olpin_spider import TerryOlpinSpider
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
process.crawl(KingsleyThomasSpider)
process.crawl(TerryOlpinSpider)
process.crawl(ChappellAndMatthewsSpider)
process.crawl(CityPropertyLetsSpider)
process.crawl(JacksonPropertySpider)
process.crawl(FlatlineSpider)
process.crawl(OceanSpider)
process.crawl(PropertyConceptSpider)
process.crawl(PurpleFrogSpider)
process.crawl(SureMoveSpider)
process.crawl(BristolPropertyCentreSpider)
process.crawl(CliftonPropertyServicesSpider)
process.crawl(AccommodationUnlimitedSpider)
process.start()