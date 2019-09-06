# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import logging
import pymongo
import json
import os
import logging
from . import settings
# for mysql
import pymysql.cursors

from TweetScraper.items import SearchItem, ProfileItem
from TweetScraper.utils import mkdirs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("insert_error.log")
fh.setLevel(logging.ERROR)
logger.addHandler(fh)


class SavetoMySQLPipeline(object):
    ''' pipeline that save data to mysql '''

    def __init__(self):
        # connect to mysql server
        self.connect = pymysql.Connect(host=settings.HOST,
                                       port=settings.PORT,
                                       user=settings.USER,
                                       passwd=settings.PASSWORD,
                                       db=settings.DB,
                                       sql_mode='')
        self.cursor = self.connect.cursor()
        self.table_name = settings.TABEL


    def find_one(self, trait, value):
        select_query = "SELECT " + trait + " FROM " + self.table_name + " WHERE " + trait + " = " + value + ";"
        try:
            val = self.cursor.execute(select_query)
        except pymysql.Error as err:
            return False

        if (val == None):
            return False
        else:
            return True

    def check_vals(self, item):
        keyword = item['keyword']
        topics = item['topics']
        publisher = item['publisher']
        nickname = item['nickname']
        content = item['content']
        url = item['url']
        like_num = item['like_num']
        comment_num = item['comment_num']
        date = item['date']
        source = item['source']

        if (keyword is None):
            return False
        elif (publisher is None):
            return False
        elif (source is None):
            return False
        elif (date is None):
            return False
        else:
            return True

    def insert_one(self, item):
        ret = self.check_vals(item)

        if not ret:
            return None

        keyword = item['keyword']
        topics = item['topics']
        publisher = item['publisher']
        nickname = item['nickname']
        content = item['content']
        url = item['url']
        like_num = item['like_num']
        comment_num = item['comment_num']
        date = item['date']
        source = item['source']

        insert_query = 'INSERT INTO ' + self.table_name + \
                       ' (keyword, topics, publisher, nickname,date, content,like_num,comment_num,url,source,subscription)'
        insert_query += ' VALUES ( %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'

        try:
            self.cursor.execute(insert_query, (
                keyword,
                topics,
                publisher,
                nickname,
                date,
                content,
                like_num,
                comment_num,
                url,
                source,
                "2"
            ))
        except pymysql.Error as err:
            logger.error(err)
        else:
            self.connect.commit()


    def process_item(self, item, spider):
        if isinstance(item, SearchItem):
            dbItem = self.find_one('content', item['content'])
            if dbItem:
                pass  # simply skip existing items
                ### or you can update the tweet, if you don't want to skip:
                # dbItem.update(dict(item))
                # self.tweetCollection.save(dbItem)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                self.insert_one(dict(item))
                logger.info("Add tweet:%s" % item['url'])


class SaveToFilePipeline(object):
    ''' pipeline that save data to disk '''

    def __init__(self):
        self.saveTweetPath = settings.SAVE_TWEET_PATH
        #self.saveUserPath = settings.SAVE_USER_PATH
        mkdirs(self.saveTweetPath)  # ensure the path exists
        #mkdirs(self.saveUserPath)

    def process_item(self, item, spider):
        if isinstance(item, SearchItem):
            savePath = os.path.join(self.saveTweetPath, item['publisher'])
            if os.path.isfile(savePath):
                pass  # simply skip existing items
                ### or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                self.save_to_file(item, savePath)
                logger.debug("Add tweet:%s" % item['url'])

        elif isinstance(item, ProfileItem):
            savePath = os.path.join(self.saveUserPath, item['ID'])
            if os.path.isfile(savePath):
                pass  # simply skip existing items
                ### or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update user:%s"%dbItem['screen_name'])
            else:
                self.save_to_file(item, savePath)
                logger.debug("Add user:%s" % item['screen_name'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))

    def save_to_file(self, item, fname):
        ''' input:
                item - a dict like object
                fname - where to save
        '''
        with open(fname, 'w') as f:
            json.dump(dict(item), f)
