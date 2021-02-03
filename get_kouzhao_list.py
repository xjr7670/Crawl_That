#-*- coding:utf-8 -*-

import json
import time
import requests


url_tpl = 'https://iszcloud-api.yun.city.pingan.com/service/show-win-detail/{}/17?cityNo=sz'

session = requests.Session()
header = {
    'Connection': 'keep-alive',
    'Host': 'iszcloud-api.yun.city.pingan.com',
    'Origin': 'https://iszcloud.yun.city.pingan.com',
    'Pragma': 'no-cache',
    'Referer': 'https://iszcloud.yun.city.pingan.com/web/release/isz-mask-notice/index.html?vt=a1_200221kzgzh',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
session.headers.update(header)
with open('kz15.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 601):
        url = url_tpl.format(i)
        print(url)
        res = session.get(url)
        data = res.json()
        data_list = data['data']['list']
        f.write('\n'.join(data_list))
        f.write('\n')
        # time.sleep(1)
    else:
        print('Finish!')
