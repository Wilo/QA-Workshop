import psycopg2


class PostgreSQLPipeline:
    def __init__(
        self,
        hostname="localhost",
        username="catalog",
        password="my_strong_and_secret_password",
        dbname="catalog",
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.dbname = dbname

    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=self.hostname,
            user=self.username,
            password=self.password,
            dbname=self.dbname,
        )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        # import ipdb

        # ipdb.set_trace()

        self.cur.execute(
            """INSERT INTO public.product_catalog
            (
                name, 
                link, 
                classification, 
                product_type, 
                brand, 
                vendor_link, 
                vendor_name, 
                vendor_sales, 
                vendor_location)
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""",
            (
                item["product"],
                item["product_link"],
                item["categoria_1"],
                item["categoria_2"],
                item["categoria_3"],
                item["vendor_link"],
                item["vendor_name"],
                item["vendor_sales"],
                item["vendor_location"],
            ),
        )
        self.connection.commit()
        return item
