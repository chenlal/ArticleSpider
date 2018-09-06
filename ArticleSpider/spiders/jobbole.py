# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request
from urllib import parse


# import urlparse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/110287/']   #获取单个文章页面的内容
    start_urls = ['http://blog.jobbole.com/all-posts/']  # 获取链接内所有连接并找到文章

    def parse(self, response):
        '''
        1.获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2.获取下一页的url并交给srapy进行下载，下载完成后交给parse
        '''

        post_nodes = response.css("#archive .floated-thumb .post-meta a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_nodes.css("::attr(href)").extract_first("")

            yield Request(parse.urljoin(response.url, post_url), meta={"front_image":image_url},
                          callback=self.parse_detail)
            # print(post_url)
        # 提取下一页并提交scrapy
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(parse.urljoin(response.url, next_url), self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段
        # xpath方式

        # title = response.xpath("//div[@class ='entry-header']/h1/text()").extract()[0]
        # creat_date = response.xpath("//p[@class = 'entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace(
        #     "·", "").strip()
        # prise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        # collection_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0].strip()
        # re_match_collection = re.match("(\d+).*", collection_nums)
        # if re_match_collection:
        #     collection_nums = re_match_collection.group(1)
        # else:
        #     collection_nums = '0'
        # comment_nums = response.xpath("//a[@href='#article-comment']/text()").extract()[0].strip()
        # re_match_collection = re.match("(\d+).*", comment_nums)
        # if re_match_collection:
        #     comment_nums = re_match_collection.group(1)
        # else:
        #     comment_nums = '0'
        # content = response.xpath("//div[@class = 'entry']").extract()
        # tag_list = response.xpath("//p[@class = 'entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = '·'.join(tag_list)
        # creator = response.xpath("//div[@class = 'copyright-area']/a/text()").extract()

        # css方式

        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        prise_nums = response.css("span.vote-post-up h10::text").extract()[0]
        collection_nums = response.css("span.bookmark-btn::text").extract()[0].strip()
        re_match_collection = re.match(".*?(\d+).*", collection_nums)
        if re_match_collection:
            collection_nums = int(re_match_collection.group(1))
        else:
            collection_nums = 0

        comment_list = response.css("a[href='#article-comment']::text").extract()
        if comment_list == []:
            comment_nums = 0
        else:
            comment_nums =comment_list[0].strip()
            re_match_collection = re.match(".*?(\d+).*", comment_nums)
            if re_match_collection:
                comment_nums = re_match_collection.group(1)
            else:
                comment_nums = 0
        creator_list = response.css(".copyright-area a::text").extract()
        creator_list = [element for element in creator_list]
        creator = "·".join(creator_list)
        content = response.css(".entry").extract()
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = '·'.join(tag_list)
        print(
            "标题：{}，作者：{}，创作日期：{}，点赞数：{}，收藏数：{}，评论数：{}".format(title, creator, create_date, prise_nums, collection_nums,
                                                              comment_nums, tags))
        # pass
        file_path = "/Users/chenjiayu/Desktop/NewFile.txt"
        with open(file_path,'a') as f:
            f.write("标题：{}，作者：{}，创作日期：{}，点赞数：{}，收藏数：{}，评论数：{}，分类：{}，链接：{}".format(title, creator, create_date, prise_nums, collection_nums,
                                                              comment_nums, tags,response.url)+'\n')
            f.close()
