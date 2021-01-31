import scrapy
from scrapy.selector import Selector
from mercadolibre.items import MercadolibreItem


class BlogSpider(scrapy.Spider):
    name = "catalogos"
    start_urls = ["https://celulares.mercadolibre.com.co/"]
    # counter = 1

    def parse(self, response):
        selector = Selector(response)
        site = selector.css(".andes-card--padding-default")
        for product in site:
            data = MercadolibreItem()
            # data['id'] = self.counter
            data["product"] = product.css("h2::text").get()
            data["product_link"] = (
                product.css("a.ui-search-item__group__element").xpath("@href").get()
            )  # noqa
            data["categoria_1"] = ""
            data["categoria_2"] = ""
            data["categoria_3"] = ""
            data["vendor_link"] = ""
            data["vendor_name"] = ""
            data["vendor_sales"] = ""
            data["vendor_location"] = ""
            # self.counter += 1
            yield data

        for next_page in response.css("a.andes-pagination__link"):
            yield response.follow(next_page, self.parse)
