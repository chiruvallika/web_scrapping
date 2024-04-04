import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ExampleSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@class="keywords"]/@content').extract_first()

            yield{
                'Text':text,
                'Author':author,
                'Tags':tags
            } 
        next_page_url =  response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']
    def parse(self, response):
        csrf_token = response.xpath('//*[@name = "csrf_token"]/@value').extract_first()
        yield FormRequest('https://quotes.toscrape.com/login',
                          formdata={'csrf_token':csrf_token,'username':'chiru','password':'123'},
                          callback = self.parse_after_login)
    def parse_after_login(self, response):
        open_in_browser(response)

class WebCrawler(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = {
        'http://books.toscrape.com/',
    }
    rules = (Rule(LinkExtractor(allow=('music')), callback='parse_page', follow=True),)

    def parse_page(self,response):
        yield {'URL':response.url}

        
    