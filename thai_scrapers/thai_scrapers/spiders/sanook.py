# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 00:35:39 2020

@author: Ruben
"""
from bs4 import BeautifulSoup
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from thai_scrapers.items import ThaiScrapersItem
from thai_scrapers.utils import contains_thai
import unicodedata

MAX_SANOOK_CO_TH_ITEM_COUNT = 250000

class SanookCoThSpider(CrawlSpider):
    """
    SanookCoThSpider is a subclass of scrapy.Spider that scrapes
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
    name = "sanook.co.th"
    allowed_domains = ['sanook.com']
    
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': MAX_SANOOK_CO_TH_ITEM_COUNT,
        # Switch to a breadth-first search which will help balance 
        # incoming data across the start_urls
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue'
        }
    
    start_urls = ['https://www.sanook.com/news/archive/',
                  'https://www.sanook.com/news/archive/entertain/',
                  'https://www.sanook.com/auto/archive/',
                  'https://www.sanook.com/hitech/archive/',
                  'https://www.sanook.com/game/archive/',
                  'https://www.sanook.com/sport/archive/',
                  'https://www.sanook.com/men/archive/',
                  'https://www.sanook.com/women/archive/',
                  'https://www.sanook.com/health/archive/',
                  'https://www.sanook.com/travel/archive/',
                  'https://www.sanook.com/horoscope/archive/',
                  'https://www.sanook.com/music/archive/',
                  'https://www.sanook.com/home/archive/',
                  'https://www.sanook.com/campus/archive/',
                  'https://www.sanook.com/movie/archive/',
                  'https://www.sanook.com/money/archive/']
    
    # List of page types allowed, as regular expressions
    # Note that the entertain subsection is listed under news
    allow_pages = ('news/\d{1,7}/$', 'auto/\d{1,7}/$', 'hitech/\d{1,7}/$',
                   'game/\d{1,7}/$', 'sport/\d{1,7}/$', 'men/\d{1,7}/$',
                   'women/\d{1,7}/$', 'health/\d{1,7}/$', 'travel/\d{1,7}/$',
                   'horoscope/\d{1,7}/$', 'music/\d{1,7}/$', 'home/\d{1,7}/$',
                   'campus/\d{1,7}/$', 'movie/\d{1,7}/$', 'money/\d{1,7}/$')
    
    # List of pages that are disallowed according to the domain's robots.txt file
    # or that we want to avoid - such as .../member/signup.php/...
    disallowed_pages = ('hot/2012_objects/.*','a/caravan7/.*','a/caravan8/.*', 'announce/.*',
                        'bookmark.php','fatherday/home/messages_ajax/.*','hot/topten/.*','/win',
                        'advertorial/.*','.*member/signup.php.*')

    # General page structure
    structure = {
        'div#EntryReader_0' : ('p','h3','ul li :not(a)'),
        'div.jsx-3971814347' : ('h1',),
        'div[itemprop = "commentText"]' : ('p',), 
        'div.jsx-3173838075 body' : ('h3','p') 
    }
    
    # Rules for following links
    rules = (
        #
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=allow_pages, deny = disallowed_pages), callback='parse_item', follow = True),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    
    def parse_item(self, response):
        # Dump some info in the log that we got to this page
        self.logger.info('Parsing %s', response.url)
        
        # Create an item object to store the scraped data
        items = []
        
        for top_level, selector_list in self.structure.items():
            for entry in response.css(top_level):
                for s in selector_list:               
                    for paragraph in entry.css(s):
                        for paragraph_text in paragraph.getall():
                            # Extract the text including HTML tags so that
                            # embedded text is not lost. For example, we want to 
                            # correctly extract "<p>I am a <strong>doctor</strong></p>"
                            # as "I am a doctor"
                            # Finally, normalize the unicode text to ensure comparable strings
                            # and strip leading and trailing white space
                            soup = BeautifulSoup(paragraph_text,'lxml')
                            clean_text = unicodedata.normalize("NFKD", soup.get_text()).strip()
                            
                            # If clean_text is non-empty and contains at least one
                            # Thai character then upload
                            if clean_text != "" and contains_thai(clean_text):
                                item = ThaiScrapersItem()
                                item['url'] = response.url
                                item['text'] = clean_text
                                items.append(item)
                            
        return items