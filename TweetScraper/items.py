# -*- coding: utf-8 -*-

# Define here the models for your scraped items
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
