# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.spider import SitemapSpider
import json


class GlobalDesiSpider(SitemapSpider):
    name = 'globaldesi'
    allowed_domains = ['globaldesi.in']
    sitemap_urls = ['https://www.globaldesi.in/sitemap.xml']
    # start_urls = [
    #     'https://www.globaldesi.in/sale-products/suits/black-printed-co-ordinates-62417.html'
    # ]

    def parse(self, response):
        pattern = r"webengage\.track\(\"GD\sProducts\sViews\",\s({.*})\);"
        try:
            txt = response.xpath("normalize-space(.//script[contains(.,'GD Products Views')]/text())").re_first(pattern)
            data = eval(txt)
            # print(data)
        except Exception as e:
            print("exception raised:", e)
            data = {}
        if "Product Ids" in data:
            id_text = "discount-percentage-{}".format(data["Product Ids"])
            discount = response.xpath(".//span[@id='" + id_text + "']/text()").extract_first()
            data['discount'] = discount
            data['url'] = response.url
            yield data

        page_links = response.xpath(".//div[@class='pages']/ol/li/a/@href").extract()
        if page_links:
            for link in page_links:
                # print(link)
                yield Request(link, callback=self.parse)
