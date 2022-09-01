from itemadapter import ItemAdapter

import psycopg2

class AppPipeline:
    def process_item(self, item, spider):
        if isinstance(item['images'], list):
            item['images'] = '\n'.join(item['images'])
        return item

class PsqlPipeline:
    def __init__(self, user, password, db, host, port=5432):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user=crawler.settings.get('POSTGRES_USER'),
            password=crawler.settings.get('POSTGRES_PASSWORD'),
            db=crawler.settings.get('POSTGRES_DB'),
            host=crawler.settings.get('POSTGRES_HOST'),
            port=crawler.settings.get('POSTGRES_PORT'),
        )

    def open_spider(self, spider):
        self._connect = psycopg2.connect(
            host=self.host,
            database=self.db,
            user=self.user,
            password=self.password,
            port=self.port
        )

        self._cursor = self._connect.cursor()


    def close_spider(self, spider):
        self._cursor.close()
        self._connect.close()

    def save_product(self, site_id, product):
        sql = ("INSERT INTO products "
            "(name, price, volume, url, img, variant_id, site_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "RETURNING id")

        self._cursor.execute(sql,
            ( product['title'], product['price'],
            product['volume'],
            product['url'], product['images'],
            product['article'], site_id )
        )

        product_id = self._cursor.fetchone()
        self._connect.commit()

        return product_id

    def process_item(self, product, spider):
        self.save_product(spider.name, product)
        return product
