# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']

    def parse(self, response):
        title = response.xpath("//div[@class ='entry-header']/h1/text()").extract()[0]
        creat_date = response.xpath("//p[@class = 'entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace(
            "·", "").strip()
        prise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        collection_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0].strip()
        re_match_collection = re.match("(\d+).*", collection_nums)
        if re_match_collection:
            collection_nums = re_match_collection.group(1)
        else:
            collection_nums = '0'
        comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract()[0].strip()
        re_match_collection = re.match("(\d+).*", comment_nums)
        if re_match_collection:
            comment_nums = re_match_collection.group(1)
        else:
            comment_nums = '0'
        content = response.xpath("//div[@class = 'entry']").extract()
        tag_list = response.xpath("//p[@class = 'entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = '·'.join(tag_list)
        creator = response.xpath("//div[@class = 'copyright-area']/a/text()").extract()
        pass
