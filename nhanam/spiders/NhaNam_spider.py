import scrapy
from urllib.parse import urljoin

class NhaNam(scrapy.Spider):
    name = 'NhaNam'
    start_urls = ['http://nhanam.com.vn/']
    domain = 'http://nhanam.com.vn/'

    def _parse(self, response, **kwargs):
        category_paths = response.xpath('//ul[@class="submenu"]/li/a/@href').getall()
        for category in category_paths:
            yield scrapy.Request(urljoin(self.domain, category), callback=self.parse_page)

    def parse_page(self, response):
        urls = response.xpath('//div[@class="wrap"]/a/@href').getall()
        book_urls = [urljoin(self.domain, u) for u in urls]

        for u in book_urls:
            yield scrapy.Request(u, callback=self.parse_book)

        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page)

    def parse_book(self, response):
        yield {
            'title': response.xpath('//a[@class="image image0"]//img/@alt').get(),
            'author': response.xpath('//li[@class="dataattr"]/a/text()').getall()[1],
            'publisher': response.xpath('//li[@class="dataattr"]/a/text()').getall()[-1],
            'image_urls' : response.xpath('//a[@class="image image0"]//img/@src').getall(),
            }


