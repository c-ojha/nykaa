# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import SitemapSpider
from scrapy.http.request import Request
import json
from urllib.parse import urlencode

class BibaSpider(scrapy.Spider):
    name = 'biba'
    allowed_domains = ['www.biba.in']
    start_urls = [
        'https://www.biba.in/new-arrivals',
        'https://www.biba.in/mix-and-match',
        'https://www.biba.in/suit-sets',
        'https://www.biba.in/girls',
        'https://www.biba.in/easy-stitch',
        'https://www.biba.in/jewellery',
        'https://www.biba.in/factory-outlet',
        'https://www.biba.in/factory-outlet'
    ]

    def parse(self, response):
        ignore_paths = [
            '/registration/', '/careers', 'sitemap', 'privacy', 'terms-of-use', 'about-us'
            '/payments-options', 'help-faq', 'delivery-and-shipping-policy', 'business-enquiries'
            '/returns-and-cancellation-policy', 'contact-us', 'trackorder', 'store-locator', '/faq/'
        ]

        pages = len(response.xpath(".//*[@class='pager']/text()").extract())
        if pages:
            # print(pages)
            pattern_match_text = r"var\sobjShowCaseInputs\s=\s({.*});"
            try:
                data = json.loads(response.xpath(".//script[@type='text/javascript']/text()").re_first(pattern_match_text))
                for i in range(1, pages + 1):
                    data['PageNo'] = i
                    # print(data)
                    encoded_url = "https://www.biba.in/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput=" + \
                                  json.dumps(data)
                    # print(encoded_url)
                    yield Request(
                        encoded_url,
                        callback=self.parse
                    )
            except Exception as e:
                print(e)

        links = set([link for link in response.xpath(".//a/@href").extract()])
        links = [link for ipath in ignore_paths for link in links
                 if (ipath not in str(link).lower().strip()) and self.allowed_domains[0] in link]
        for link in links:
            # print(link)
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
