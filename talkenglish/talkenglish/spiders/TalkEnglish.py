# -*- coding: utf-8 -*-
import os
from pathlib import Path
import scrapy
from scrapy.http import Request


class TalkenglishSpider(scrapy.Spider):
    name = 'TalkEnglish'
    allowed_domains = ['talkenglish.com']
    start_urls = ['https://www.talkenglish.com/listening/listenbasic.aspx',
                  'https://www.talkenglish.com/listening/listenintermediate.aspx',
                  'https://www.talkenglish.com/listening/listenadvanced.aspx']

    def parse(self, response):
        # 分别获取3个等级的页面中的所有听力练习页面的地址

        root = response.xpath('//div[@class="steps-learn"]')[0]
        level = root.xpath('./b/a/text()').extract_first()
        if not os.path.exists(level):
            os.mkdir(level)
        lesson_list = []
        a_lists = root.xpath('./div/a')
        for a_tag in a_lists:
            lesson_name = a_tag.xpath('text()').extract_first()
            relative_lesson_url = a_tag.attrib['href']
            lesson_url = response.urljoin(relative_lesson_url)
            # yield Request(url=lesson_url,
            #               callback=self.parse_detail,
            #               meta={'level': level, 'title': lesson_name})
            lesson_list.append((level, lesson_name, lesson_url))
            print('Title: %s\tURL: %s' % (lesson_name, lesson_url))

    def parse_detail(self, response):

        meta = response.meta
        root_div = response.xpath('//div[@class="sm2-playlist-bd"]')[0]
        mp3_url = root_div.xpath('.//a').attrib['href']
        yield Request(url=mp3_url,
                      callback=self.download_mp3,
                      meta=meta)

    def download_mp3(self, response):

        level = response.meta['level']
        title = response.meta['title'].replace('#', '').replace(' ', '_')
        title += '.mp3'
        pwd = Path()
        with open(pwd.joinpath(level, title), 'wb') as mp3:
            mp3.write(response.body)
