'''
2017/3/20
爬取jekunauto.com网站上的服务产品项目及其价格

不需要登录
需要使用第三方包lxml和requests
'''

import requests
from time import sleep
from lxml import etree

url = "http://www.jekunauto.com/product/category/index"
res = requests.get(url)
source = res.text

root = etree.HTML(source)
category_div = root.xpath('//div[@class="jk-list-wrap"]')

cat_name = list()
cat_url = list()
for each_div in category_div:
    categorys = each_div.findall('./a')
    for category in categorys:
        name = category.text
        url = category.get('href')
        cat_name.append(name)
        cat_url.append(url)

base_url = "http://www.jekunauto.com/v1/goods?service_id="
goods_name_list = list()
price_list = list()

i = 0

for n, u in zip(cat_name, cat_url):
    print(n)
    id = u.split('/')[3]
    xml_url = base_url + str(id)
    xml_res = requests.get(xml_url)
    xml_sou = xml_res.text

    xml = xml_sou.replace('true', '"true"').replace('null', '"null"')
    xml_dict = eval(xml)

    data = xml_dict['data']
    for item in data:
        goods_name = item['goods_name']
        price = item['preferential_price']

        print('\t' + str(i) + '\t' + goods_name + '\t-----\t' + price)

        goods_name_list.append(goods_name)
        price_list.append(price)
        i += 1
    sleep(3)
else:
    with open('result', 'w') as f:
        for g, p in zip(goods_name_list, price_list):
            f.write("%s\t%s\n" % (g, p))
