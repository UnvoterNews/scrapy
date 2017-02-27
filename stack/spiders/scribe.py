import scrapy
import sys
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.conf import settings
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from stack.items import StackItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import XmlXPathSelector
from scrapy.spiders import XMLFeedSpider

class LibertarianRSS(XMLFeedSpider):
    name = 'stack'
    allowed_domains = ['libertarianinstitute.org']
    start_urls = ['https://www.libertarianinstitute.org/articles/feed/']
    namespaces = [('dc', 'http://purl.org/dc/elements/1.1/'),('content','http://purl.org/rss/1.0/modules/content/')]
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        #self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))
        response.selector.remove_namespaces()
        item = StackItem()
        item['title'] = node.xpath('normalize-space(title/text())').extract()
        item['url'] = node.xpath('link/text()').extract()
        item['authorname'] = node.xpath('dc:creator/text()').extract()
        item['publicationdate'] = node.xpath('pubdate/text()').extract()
        item['desc'] = node.xpath('description/text()').extract()
        item['content'] = node.xpath('content:encoded/text()').extract()
        yield item

class ReasonorgRSS(XMLFeedSpider):
    name = 'stack'
    allowed_domains = ['reason.org']
    start_urls = ['http://reason.org/news/index.xml']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        #self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = StackItem()
        item['title'] = node.xpath('title/text()').extract()
        item['url'] = node.xpath('link/text()').extract()
        item['authorname'] = node.xpath('author/text()').extract()
        item['publicationdate'] = node.xpath('pubDate/text()').extract()
        item['desc'] = ''
        item['content'] = node.xpath('description/text()').extract()
        
        yield item

class EllenbrownRSS(XMLFeedSpider):
    name = 'stack'
    allowed_domains = ['ellenbrown.com']
    start_urls = ['https://ellenbrown.com/feed/']
    namespaces = [('dc','http://purl.org/dc/elements/1.1/'),('media','http://search.yahoo.com/mrss/')]
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        #self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))
        response.selector.remove_namespaces()
        item = StackItem()
        item['title'] = node.xpath('title/text()').extract()
        item['url'] = node.xpath('link/text()').extract()
        item['authorname'] = node.xpath('dc:creator/text()').extract()
        item['authorurl'] = node.xpath('guid/text()').extract()
        item['publicationdate'] = node.xpath('pubDate/text()').extract()
        item['content'] = node.xpath('description/text()').extract()
        


        yield item

class AntiwarSpider(Spider):
    name = "stack"
    allowed_domains = ["antiwar.com"]
    start_urls = ["https://www.antiwar.com/blog/"]
#Link extractors are objects whose only purpose is to extract links from web pages     
    rules = (Rule(LxmlLinkExtractor(allow=()), callback="parse", follow=True),)

#Main method invoked from the crawler- can be overriden if needed 
    def parse(self, response):
        questions = Selector(response).xpath('//main[@class="site-main"]/article')
        #print "guru"+str(questions)
        for question in questions:


            item = StackItem()
            item['title'] = question.xpath(
                'header/h2/a/text()').extract()
            item['url'] = question.xpath(
                'header/h2/a/@href').extract()
            item['authorname'] = question.xpath('footer/span/span/a[@class="url fn n"]/text()').extract()
            item['authorurl'] = question.xpath('footer/span/span/a[@class="url fn n"]/@href').extract()
            item['publicationdate'] = question.xpath('footer/span/a/time[@class="entry-date published updated"]/text()').extract()
            item['content'] = question.xpath('div[@class="entry-content"]/p/text()').extract()

            yield item

        
       
class KasparovSpider(Spider):
    name = "stack"
    allowed_domain=['kasparov.com']
    start_urls = [
           
            "http://www.kasparov.com/blog-2/"
        ]
        
    rules = (Rule(LxmlLinkExtractor(allow=()), callback="parse", follow= True),)
    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="post-title"]')

        for question in questions:
            #print question
            #iprint 'guru'
            item = StackItem()
            item['title'] = question.xpath(
                'a/text()').extract()
            item['url'] = question.xpath(
                'a/@href').extract()[0]
            yield item 
        for link in LxmlLinkExtractor(allow=()).extract_links(response):
            yield Request(link.url, callback=self.parse_page)

    def parse_page(self, response):
        paras = Selector(response).xpath('//div/p')
        for para in paras:
            item = StackItem()
            item['url']=response.url
            item['desc']= para.xpath('text()').extract()
            yield item
     
       

        
class ReasonSpider(Spider):
    name = "stack"
    allowed_domains = ["reason.org"]
    start_urls = ["http://reason.org/"]
    rules = (Rule(LxmlLinkExtractor(allow=()), callback="parse", follow=True),)
    def parse(self, response):
        sites = Selector(response).xpath('//div/h4')
        for site in sites:
            item = StackItem()
            print site
            item['title'] = site.xpath("a/text()").extract() 
            item['url'] = 'http://reason.org'+str(site.xpath("a/@href").extract_first()) 
            #item['description'] = site.xpath("following-sibling::div/text()").extract_first('').strip()
            yield item

        for link in LxmlLinkExtractor(allow=()).extract_links(response):
            yield Request(link.url, callback=self.parse_page)
     


    def parse_page(self, response):
        paras = Selector(response).xpath('//div/p')
        for para in paras:
            item = StackItem()
            item['url'] = response.url
            item['desc'] = para.xpath('text()').extract() 
            yield item 
        
configure_logging()
runner = CrawlerRunner(get_project_settings())

# This part is where we set up spiders sequentially for crawling. Keep adding new classes created here
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(LibertarianRSS)
    yield runner.crawl(ReasonorgRSS)
    yield runner.crawl(EllenbrownRSS)
    #yield runner.crawl(AntiwarSpider)
    
    #yield runner.crawl(KasparovSpider)
    #yield runner.crawl(ReasonSpider)
    reactor.stop()
    


crawl()
try:
   reactor.run() # the script will block here until the last crawl call is finished'
except:
    print "expected runner still running:", sys.exc_info()[0]
    print "Spiders Execution Completed"
