from scrapy.crawler import CrawlerProcess
from TweetScraper.spiders.TweetCrawler import TweetScraper

process=CrawlerProcess()
process.crawl(TweetScraper,query="hongkong")
process.start()