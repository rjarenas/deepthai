# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 11:04:52 2020

@author: Ruben
"""
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from thai_scrapers.items import ThaiScrapersItem
import re
import unicodedata
from thai_scrapers.utils import contains_thai

MAX_TH_WIKIPEDIA_ORG_COUNT = 10000

class ThWikipediaSpider(Spider):
    """
    ThWikipediaSpider is a subclass of scrapy.Spider that scrapes
    the website sanook.co.th.

    Attributes
    ----------
    name : str
        the name of the Spider, "sanook.co.th", used for calling the Spider
        from the commandline
    
    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    name = "th.wikipedia.org"
    allowed_domains = ['th.wikipedia.org']
    
    # Wikipedia is particular that it only allows "slow" crawling
    download_delay = 2
        
    custom_settings = {
        #'CLOSESPIDER_ITEMCOUNT': MAX_TH_WIKIPEDIA_ORG_COUNT,
        # Will obey robots.txt through explicit code
        'ROBOTSTXT_OBEY' : True,
        'CONCURRENT_REQUESTS_PER_IP' : 5
        }
    
    # English translation of start urls:
    # Beliefs
    # Technology
    # Nature
    # Entertainment
    # Thailand
    # History
    # Geography
    # Science
    # Art
    # Society
    
    start_urls = [
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%84%E0%B8%A7%E0%B8%B2%E0%B8%A1%E0%B9%80%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B9%80%E0%B8%97%E0%B8%84%E0%B9%82%E0%B8%99%E0%B9%82%E0%B8%A5%E0%B8%A2%E0%B8%B5',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%98%E0%B8%A3%E0%B8%A3%E0%B8%A1%E0%B8%8A%E0%B8%B2%E0%B8%95%E0%B8%B4',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9A%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%97%E0%B8%B4%E0%B8%87',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%A7%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B8%A8%E0%B8%B2%E0%B8%AA%E0%B8%95%E0%B8%A3%E0%B9%8C',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%A0%E0%B8%B9%E0%B8%A1%E0%B8%B4%E0%B8%A8%E0%B8%B2%E0%B8%AA%E0%B8%95%E0%B8%A3%E0%B9%8C',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%A7%E0%B8%B4%E0%B8%97%E0%B8%A2%E0%B8%B2%E0%B8%A8%E0%B8%B2%E0%B8%AA%E0%B8%95%E0%B8%A3%E0%B9%8C',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%A8%E0%B8%B4%E0%B8%A5%E0%B8%9B%E0%B8%B0',
        'https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%84%E0%B8%A1']
    
    # List of page types allowed, as regular expressions
    allow_pages = ('/wiki/.*',)
    
    #List of pages that are disallowed according to the domain's robots.txt file
    disallowed_pages = ('.*\.php','.*/w/.*','.*/api/.*','.*/trap/.*', 
        '.*%E0%B8%AA%E0%B8%96%E0%B8%B2%E0%B8%99%E0%B8%B5%E0%B8%A2%E0%B9%88%E0%B8%AD%E0%B8%A2:.*',
        '.*%E0%B9%81%E0%B8%A1%E0%B9%88%E0%B9%81%E0%B8%9A%E0%B8%9A:.*',
        #วิกิพีเดีย:
        '.*%E0%B8%A7%E0%B8%B4%E0%B8%81%E0%B8%B4%E0%B8%9E%E0%B8%B5%E0%B9%80%E0%B8%94%E0%B8%B5%E0%B8%A2:.*'
        )

    # General page structure
    structure = {
        'div#mw-content-text' : ('div.mw-parser-output>p','dl dd'),
        }
    
    # Structure of links we want to extract
    link_structure = {
        'div.mw-parser-output table' : ('div.hlist a::attr(href)',),
        'div.mw-category' : ('a::attr(href)',),
        'div#mw-subcategories' : ('a::attr(href)',),
        'div#mw-pages' : ('a::attr(href)',)
        }
    
    # Tags that should be explicitly removed, with all their content, from scraped material
    exclude_tags = ('sup','math','img')
       
    def parse(self, response):       
        # Precompile regular expressions
        
        #Find relevant links on the page and yield new requests from them
        for top_level, selector_list in self.link_structure.items():
            for entry in response.css(top_level):
                for s in selector_list:
                    for link in entry.css(s).getall():
                        # Check that the link is allowable and not disallowed 
                        allowed = False
                        disallowed = False
                        
                        for allowed_page in self.allow_pages:
                            if re.search(allowed_page, link) is not None:
                                allowed = True
                        
                        for disallowed_page in self.disallowed_pages:
                            if re.search(disallowed_page,link) is not None:
                                disallowed = True
                        
                        if allowed and not disallowed:
                            yield response.follow(url = link, callback = self.parse)
                                
                                
        
        # Create an item object to store the scraped data        
        for top_level, selector_list in self.structure.items():
            for entry in response.css(top_level):
                for s in selector_list:               
                    for paragraph in entry.css(s):
                        for paragraph_text in paragraph.getall():
                            # Extract the text including HTML tags so that
                            # embedded text is not lost. For example, we want to 
                            # correctly extract "<p>I am a <strong>doctor</strong></p>"
                            # as "I am a doctor"
                            soup = BeautifulSoup(paragraph_text,'lxml')
                            
                            # Remove context for tags that aren't actually text,
                            # for example, citations (sup tag)
                            for tag in self.exclude_tags:
                                for tag_content in soup(tag):
                                    tag_content.decompose()
                            
                            # Finally, normalize the unicode text to ensure comparable strings
                            # and strip leading and trailing white space
                            clean_text = unicodedata.normalize("NFKD", soup.get_text()).replace('\u200b', '').replace('\n', '').strip()
                            
                            # If clean_text is non-empty and contains at least one
                            # Thai character then upload
                            if clean_text != "" and contains_thai(clean_text):
                                yield ThaiScrapersItem(url = response.url, text = clean_text)

