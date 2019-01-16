# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import SitemapSpider
from scrapy.http.request import Request
import json

class BibaSpider(scrapy.Spider):
    name = 'biba'
    allowed_domains = ['www.biba.in']
    start_urls = ['https://www.biba.in/']
    # sitemap_urls = [
    #     'https://www.biba.in/'
    # ]

    def parse(self, response):
        ignore_paths = [
            '/registration/', '/careers', 'sitemap', 'privacy', 'terms-of-use', 'about-us'
            '/payments-options', 'help-faq', 'delivery-and-shipping-policy', 'business-enquiries'
            '/returns-and-cancellation-policy', 'contact-us', 'trackorder', 'store-locator', '/faq/'
        ]
        links = set([link for link in response.xpath(".//a/@href").extract()])
        links = [link for ipath in ignore_paths for link in links
                 if (ipath not in str(link).lower().strip()) and self.allowed_domains[0] in link]
        for link in links:
            print(link)
            if '/p/' in link:
                yield Request(link, callback=self.extract_items)
            if self.allowed_domains[0] in link:
                yield Request(link, callback=self.parse)

    def extract_items(self, response):
        pattern_match_text = r"MartJack\s=({.*})"
        data = response.xpath(".//script[@type='text/javascript']/text()").re_first(pattern_match_text)
        product = json.loads(data)['PageInfo']
        if product['PageType'] == 'product':
            product['url'] = response.url
            yield product
