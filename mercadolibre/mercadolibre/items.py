# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadolibreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    product = scrapy.Field()
    product_link = scrapy.Field()
    categoria_1 = scrapy.Field()
    categoria_2 = scrapy.Field()
    categoria_3 = scrapy.Field()
    vendor_link = scrapy.Field()
    vendor_name = scrapy.Field()
    vendor_sales = scrapy.Field()
    vendor_location = scrapy.Field()
