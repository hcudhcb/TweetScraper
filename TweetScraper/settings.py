# -*- coding: utf-8 -*-
import random
# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT_LIST =[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
USER_AGENT =  random.choice(USER_AGENT_LIST)
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
COOKIES_ENABLES=False
# settings for spiders
BOT_NAME = 'TweetScraper'
LOG_LEVEL = 'INFO'
DOWNLOAD_HANDLERS = {'s3': None,} # from http://stackoverflow.com/a/31233576/2297751, TODO
CLOSESPIDER_ITEMCOUNT=20
SPIDER_MODULES = ['TweetScraper.spiders']
NEWSPIDER_MODULE = 'TweetScraper.spiders'
ITEM_PIPELINES = {
    #'TweetScraper.pipelines.SavetoMySQLPipeline':100,
    #'TweetScraper.pipelines.SaveToFilePipeline':100
    #'TweetScraper.pipelines.SaveToMongoPipeline':100, # replace `SaveToFilePipeline` with this to use MongoDB
    #'TweetScraper.pipelines.SavetoMySQLPipeline':100, # replace `SaveToFilePipeline` with this to use MySQL
}

# settings for where to save data on disk
SAVE_TWEET_PATH = './Data/tweet/'
#SAVE_USER_PATH = './Data/user/'

# settings for mongodb
MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "TweetScraper"        # database name to save the crawled data
MONGODB_TWEET_COLLECTION = "tweet" # collection name to save tweets
#MONGODB_USER_COLLECTION = "user"   # collection name to save users
# settings for mysql
HOST = "10.60.1.76"
PORT = 3306
USER = "ft_clawer"
PASSWORD = "ft_clawer"
DB = "ft_clawer"
TABEL = "search_item"


