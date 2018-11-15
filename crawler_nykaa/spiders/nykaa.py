# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
import json


class NykaaSpider(scrapy.Spider):
    name = 'nykaa'
    allowed_domains = ['nykaa.com']
    base_url = 'https://www.nykaa.com/gludo/products/list'
    params = {
        "category_id": 24,
        "order": "popularity",
        "page_no": 1
    }

    def start_requests(self):
        yield Request(
            self.base_url + "?" + urlencode(self.params),
            callback=self.generate_urls_by_cat
        )

    def generate_urls_by_cat(self, response):
        data = json.loads(response.body_as_unicode())
        for category in data['result']['filters']['category']:
            count = int(category['count'])
            page_size = int(count/20) + 1 if count % 20 else int(count/20)
            for p in range(0, page_size):
                self.params.update({
                    'category_id': category['category_id'],
                    'page_no': p+1
                })
                request = Request(
                    self.base_url + '?' + urlencode(self.params),
                    callback=self.parse
                )
                request.meta['cat'] = category.copy()
                yield request

    def parse(self, response):
        cat = response.meta['cat']
        data = json.loads(response.body_as_unicode())
        for product in data['result']['products']:
            p = product.copy()
            if "category_values" in p:
                del p["category_values"]
            if "category_ids" in p:
                del p["category_ids"]
            p['category_name'] = cat['name']
            p['category'] = cat
            yield p
