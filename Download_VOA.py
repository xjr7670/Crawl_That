'''
Get VOA Learning English Broadcast broadcast mp3 file
By: Caivn
Date: 2017/07/22
Version: 1
'''

import requests
import xmltodict
import time

url = "https://learningenglish.voanews.com/podcast/?count=20&zoneId=1689"
res = requests.get(url)
src = res.text

doc = xmltodict.parse(src)
items = doc['rss']['channel']['item']
length = len(items)

names = []
urls = []

for item in items:
    name = item['title']
    url = item['enclosure']['@url']
    names.append(name)
    urls.append(url)

for n, u in zip(names, urls):
    print('Downloading %s\n' % n)
    print('\t%s' % u)
    r = requests.get(u, stream=True)
    with open('VOA\\' + n + '.mp3', 'wb') as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)
    time.sleep(3)
