# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy


#class StackItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass

from scrapy.item import Item, Field


class StackItem(Item):
    title = Field()
    url = Field()
    timestamp = Field()
    desc = Field()   
    subtitle = Field()
    exceprt = Field()
    authorname = Field()
    authorurl = Field()
    authortwitter = Field()
    mediaurl = Field()
    mediacaption = Field()
    mediaattribute = Field()
    publicationname = Field()
    publicationurl = Field()
    publicationdate = Field()
    publicationlocation= Field()
    publicationsource = Field()
    content = Field()
    htmlraw = Field()
