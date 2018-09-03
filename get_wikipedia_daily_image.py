# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 16:12:12 2018

@author: Administrator
"""

import re
from datetime import datetime
import requests
import xmltodict


class Wiki:
    
    def __init__(self):
        
        self.url_pat = re.compile(r'src="(.*?)"')
        self.des_pat = re.compile(r'<[^>]+>')
        self.day_pat = re.compile(r'[^\d]')

    def make_day(self, title_src):
        
        now = datetime.now()
        year = now.year
        md = self.day_pat.sub('', title_src)
        
        if len(md) == 2:
            md = '0' +'0'.join(md)
        elif len(md) == 3:
            md = '0' + md
        
        full_day = str(year) + md
        
        return full_day
        
    
    def get_image(self):
        
        url = 'https://wk.mekaku.com/w/api.php?action=featuredfeed&feed=potd&format=xml'
        res = requests.get(url)
        src = res.text
        
        root = xmltodict.parse(src)
        items = root['rss']['channel']['item']
        
        for item in items:
            title = item['title'].strip()
            img_src = self.url_pat.search(item['description'])
            
            # some day there are not image
            # if there have
            if img_src:
                description = self.des_pat.sub('', item['description'])
                print(title, description.strip(), self.make_day(title))


if __name__ == '__main__':
    wiki = Wiki()
    wiki.get_image()