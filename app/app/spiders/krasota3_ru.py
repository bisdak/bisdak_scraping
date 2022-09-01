from operator import ne
import scrapy
from app.items import Product

from pprint import pprint


class Krasota3RuSpider(scrapy.Spider):
    name = 'krasota3.ru'
    domain = 'https://krasota3.ru/'
    allowed_domains = ['krasota3.ru']
    start_urls = ['https://krasota3.ru/kosmetika-gigi-kupit/']

    custom_settings = {
        'COOKIES_ENABLED': True
    }


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'beget': 'begetok'}, callback=self.parse_main)

    def parse_main(self, response):
        for category_link in response.css('.product a::attr(href)').getall():
            link = self.domain+category_link
            yield scrapy.Request(link, cookies={'beget': 'begetok'}, callback=self.parse_category)

        next_page = self.find_next_page(response)
        if next_page is not None:
            yield scrapy.Request(next_page, cookies={'beget': 'begetok'}, callback=self.parse, 
                                 dont_filter=True)


    def parse_category(self, response):
        product_links = response.css('.product-name::attr(href)').getall()

        for product_link in product_links:
            product_link = self.domain + product_link
            yield scrapy.Request(product_link, cookies={'beget': 'begetok'}, callback=self.parse_product)

    def parse_product(self, response):
        p = Product()

        p['article'] = response.css('.acticul span::text').get()
        p['title'] = response.css('h1.heading::text').get()
        p['product_line'] = response.css('.breadcrumb li span[itemprop=name]::text').getall()[-2]
        
        p['images'] = response.css('#image-block .img-responsive::attr(src)').get()

        p['barcode'] = None
        p['composition'] = None
        p['url'] = response.url
        p['currency'] = None

        description_titles = response.css('.text-content h2::text')
        for idx, title in enumerate(description_titles):
            # words = response.css('.text-content p::text').re('[а-яА-Я]+')
            words = title.re('[а-яА-Я]+')
            words = list(map(lambda w: w.lower(), words))

            if 'состав' in words:
                print(words)
                try:
                    p['composition'] = response.css('.text-content p::text').getall()[idx]
                except IndexError:
                    pass

        p['weight'] = None
        for label in response.css('.form-group .flex label'):
            p['price'] = label.css('span::text').get().replace(' ', '')
            p['volume'] = label.css(':not(span) *::text').getall()[-1].strip()

            yield p


    def find_next_page(self, response):
        pagination_links = response.css('.page-item:not(.disabled) a')
        for el in pagination_links:
            if el.css('::text') == '»':
                return el.css('::attr(href)').get()
        return None