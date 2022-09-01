import scrapy


class Product(scrapy.Item):
    title = scrapy.Field()
    product_line = scrapy.Field()
    volume = scrapy.Field()
    weight = scrapy.Field()
    price = scrapy.Field()
    article = scrapy.Field()
    barcode = scrapy.Field()
    composition = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()