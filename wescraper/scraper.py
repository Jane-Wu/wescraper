from wespider import WeSpider
from scrapy.crawler import CrawlerProcess
import config

class WeScraper:
    """
    WeScraper can search official articles and return data in Json format
    """
    results = []

    def process_item(self, item, spider):
        self.results.append(dict(item))

    def crawl_key(self, search_type, accounts):
        crawler = CrawlerProcess({
            'ITEM_PIPELINES'           : {'__main__.WeScraper' : 1},
            'COOKIES_ENABLED'          : True,
            'RANDOMIZE_DOWNLOAD_DELAY' : True,
            'ACCOUNT_LIST'             : accounts,
            'SEARCH_TYPE'              : search_type
        })
        spider = WeSpider()
        crawler.crawl(spider)
        crawler.start()
        return sorted(self.results, key=lambda x:x[u'date'], reverse=True)

if __name__ == '__main__':
    import sys
    datas = []
    if len(sys.argv) > 1 and sys.argv[1] in config.types:
        datas = WeScraper().crawl_key(sys.argv[1], sys.argv[2:])
        import json
        print json.dumps(datas, ensure_ascii=False).encode("utf8")
    else:
        print "Search type can only be {}".format(str(config.types))
