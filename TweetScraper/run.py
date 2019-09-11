from scrapy.crawler import CrawlerProcess
from TweetScraper.spiders.TweetCrawler import TweetScraper
from scrapy.utils.project import get_project_settings

process=CrawlerProcess(get_project_settings())
spider_tweet = TweetScraper()
process.crawl(spider_tweet,query="hongkong")
process.start()