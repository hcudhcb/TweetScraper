# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# from scrapy import Item, Field
#
#
# class Tweet(Item):
#     ID = Field()       # tweet id
#     url = Field()      # tweet url
#     datetime = Field() # post time
#     text = Field()     # text content
#     user_id = Field()  # user id
#     usernameTweet = Field() # username of tweet
#
#     nbr_retweet = Field()  # nbr of retweet
#     nbr_favorite = Field() # nbr of favorite
#     nbr_reply = Field()    # nbr of reply
#
#     is_reply = Field()   # boolean if the tweet is a reply or not
#     is_retweet = Field() # boolean if the tweet is just a retweet of another tweet
#
#     has_image = Field() # True/False, whether a tweet contains images
#     images = Field()    # a list of image urls, empty if none
#
#     has_video = Field() # True/False, whether a tweet contains videos
#     videos = Field()    # a list of video urls
#
#     has_media = Field() # True/False, whether a tweet contains media (e.g. summary)
#     medias = Field()    # a list of media
#
#
# class User(Item):
#     ID = Field()            # user id
#     name = Field()          # user name
#     screen_name = Field()   # user screen name
#     avatar = Field()        # avator url
#
import scrapy


class SearchItem(scrapy.Item):
    keyword = scrapy.Field()  # 搜索关键字
    topics = scrapy.Field(serializer=str)  # 帖子的话题，可能多个，array
    publisher = scrapy.Field()  # 能够链接到用户主页的用户名
    nickname = scrapy.Field()  # 帖子展示的昵称，可能与用户名不同
    date = scrapy.Field()  # formated: yyyy-MM-dd HH:mm
    content = scrapy.Field()
    like_num = scrapy.Field()
    comment_num = scrapy.Field()
    url = scrapy.Field()  # 查看帖子详情的地址
    source = scrapy.Field()  # 信息来源：Facebook/Twitter


class ProfileItem(scrapy.Item):
    username = scrapy.Field()  # url上的用户名
    nickname = scrapy.Field()  # 主页展示上的昵称，与用户名可能不同
    profile = scrapy.Field(serializer=str)  # 个人信息，K:V结构
    follow_num = scrapy.Field()  # 关注的用户的数量
    follower_num = scrapy.Field()  # 粉丝数
    source = scrapy.Field()
