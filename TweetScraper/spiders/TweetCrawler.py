from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from .. import settings
from scrapy import http
from scrapy.shell import inspect_response  # for debugging
import re
import json
import os
import time
import logging
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from datetime import datetime

from TweetScraper.items import SearchItem,ProfileItem
from .. import utils

logger = logging.getLogger(__name__)
fh = logging.FileHandler('crawl_tweet.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
#执行方法：scrapy crawl TweetScraper -a query="hongkong"
class TweetScraper(CrawlSpider):
    name = 'TweetScraper'

    allowed_domains = ['twitter.com']
    def __init__(self, query='', lang='', top_tweet=False):
        self.proxy = "socks5://172.22.0.24:7012"
        self.query = query
        self.url = "https://twitter.com/i/search/timeline?l={}".format(lang)

        self.api = utils.create_api()
        if not top_tweet:
            self.url = self.url + "&f=tweets"

        self.url = self.url + "&q=%s&src=typed&max_position=%s"



    def start_requests(self):

        url = self.url % (quote(self.query), '')
        yield http.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # inspect_response(response, self)
        # handle current page
        data = json.loads(response.body.decode("utf-8"))
        print(data)
        for item in self.parse_tweets_block(data['items_html']):
            yield item

        # get next page
        min_position = data['min_position']
        min_position = min_position.replace("+","%2B")
        url = self.url % (quote(self.query), min_position)
        yield http.Request(url, callback=self.parse_page)

    def parse_tweets_block(self, html_page):
        page = Selector(text=html_page)

        ### for text only tweets
        items = page.xpath('//li[@data-item-type="tweet"]/div')
        for item in self.parse_tweet_item(items):
            yield item

    def parse_tweet_item(self, items):
        count = 0
        for item in items:
            count = count+1
            try:
                tweet = SearchItem()
                logger.info("Start crawling "+ str(count)+"th item")
                tweet['keyword'] = self.query
                tweet['topics'] = ""
                topics = item.xpath('.//div[@class="js-tweet-text-container"]/p[@class="TweetTextSize  js-tweet-text tweet-text"]/a[@data-query-source="hashtag_click"]/b//text()').extract()
                if len(topics) >0:
                    for topic in topics:
                        tweet['topics']=tweet['topics']+ ','
                        tweet['topics'] = tweet['topics']+topic
                    tweet['topics'] = tweet['topics'][1:]
                else:
                    tweet['topics'].join(" ")
                tweet['publisher'] = item.xpath('.//span[@class="username u-dir u-textTruncate"]/b//text()').extract()[0]
                tweet['nickname'] = item.xpath('.//strong[@class="fullname show-popup-with-id u-textTruncate "]//text()').extract()[0]
                # ID = item.xpath('.//@data-tweet-id').extract()
                # if not ID:
                #     continue
                # tweet['ID'] = ID[0]

                ### get text content
                tweet['content'] = ' '.join(
                    item.xpath('.//div[@class="js-tweet-text-container"]/p//text()').extract()).replace(' # ',
                                                                                                        '#').replace(
                    ' @ ', '@')
                if tweet['content'] == '':
                    # If there is not text, we ignore the tweet
                    continue

                ### get meta data
                tweet['url'] = "https://twitter.com"+item.xpath('.//@data-permalink-path').extract()[0]

                # nbr_retweet = item.css('span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount').xpath(
                #     '@data-tweet-stat-count').extract()
                # if nbr_retweet:
                #     tweet['nbr_retweet'] = int(nbr_retweet[0])
                # else:
                #     tweet['nbr_retweet'] = 0

                like = item.css('span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount').xpath(
                    '@data-tweet-stat-count').extract()
                if like:
                    tweet['like_num'] = int(like[0])
                else:
                    tweet['like_num'] = 0

                reply = item.css('span.ProfileTweet-action--reply > span.ProfileTweet-actionCount').xpath(
                    '@data-tweet-stat-count').extract()
                if reply:
                    tweet['comment_num'] = int(reply[0])
                else:
                    tweet['comment_num'] = 0

                tweet['date'] = datetime.fromtimestamp(int(
                    item.xpath('.//div[@class="stream-item-header"]/small[@class="time"]/a/span/@data-time').extract()[
                        0])).strftime('%Y-%m-%d %H:%M:%S')
                tweet['source'] = "Twitter"

                yield tweet
                logger.info("End crawling the "+str(count)+"th item")
            except:
                logger.error("Error tweet:\n%s" % item.xpath('.').extract()[0])
                # raise

    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default
