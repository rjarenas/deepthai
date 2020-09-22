# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:01:49 2020

@author: Ruben
"""

import scrapy
from scrapy.crawler import CrawlerProcess

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    outputResponse = []
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            self.outputResponse = self.outputResponse.append(response.css("span.text::text").extract_first())
            yield self.outputResponse[-1]
            
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
            
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

text = []
process.crawl(ToScrapeCSSSpider, outputResponse = text)
process.start()

