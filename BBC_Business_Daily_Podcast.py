'''
Time: 2017/3/3
Author: Cavin
Library need: lxml requests

Target: From url: http://www.bbc.co.uk/programmes/p002vsxs/episodes/downloads download the news' mp3 media on the page.
        Use the news' title as the file name to save to local and will replace some irregular symbol. And replace the space with single underline.
        Some news do not have download link. This program will only download which can download
'''

import re
import requests
from time import sleep
from lxml import etree

res = requests.get("http://www.bbc.co.uk/programmes/p002vsxs/episodes/downloads")
html = res.text

root = etree.HTML(html)

div = root.xpath('//div[@class="component__body br-box-page"]/ul')


li_list = div[0].findall('./li')

item = dict()
title_pat = re.compile(r'[:?*"!< >]+')

for li in li_list:
    title = li.find('.//span[@property="name"]')
    name = title.text
    name = title_pat.sub('_', name)
    link = li.find('.//ul[@class="list-unstyled popup__list"]/li')
    if link is not None:
        url = link.find('./a').attrib['href']
        item[name] = url

for k, v in item.items():
    print('Request for %s' % k)
    res = requests.get(v, stream=True)
    with open(k + '.mp3', 'wb') as music_f:
        for chunk in res.iter_content(chunk_size=50000):
            music_f.write(chunk)
    sleep(3)
else:
    print('Finish!')
