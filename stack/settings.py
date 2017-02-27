# -*- coding: utf-8 -*-

# Scrapy settings for stack project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'stack'

SPIDER_MODULES = ['stack.spiders']
NEWSPIDER_MODULE = 'stack.spiders'

CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 16


ITEM_PIPELINES = {'stack.pipelines.MongoDBPipeline': 300}
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "scrapy"
MONGODB_COLLECTION = "news"
MONGODB_ADD_TIMESTAMP = True



#ROBOTSTXT_OBEY = True


SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
    
}
DELTAFETCH_ENABLED = True



