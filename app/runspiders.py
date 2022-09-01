from scrapy import spiderloader
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

SKIP_SPIDERS = ['LiderMartRuSpider']

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

# Get all spider class name
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
spiders = spider_loader.list()
classes = [spider_loader.load(name) for name in spiders]


@defer.inlineCallbacks
def crawl():
    for obj in classes:
        if obj.__name__ in SKIP_SPIDERS:
            continue
        yield runner.crawl(obj)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished