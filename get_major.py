# -*- coding:utf-8 -*-

import sys
import math
import requests


class parseMajor:

    def __init__(self):
        self.session = requests.Session()

    def update_headers(self, headers):
        self.session.headers.update(headers)

    def get_major_name(self, school_code, page=1):

        ret = []
        url_params = {
            'year': 2019,
            'code': school_code,
            'page': page 
        }

        # https://static-data.eol.cn/www/2.0/schoolspecialindex/2019/1739/45/1/10/2.json
        url = ('https://static-data.eol.cn/www/2.0/schoolspecialindex'
                '/{year}/{code}/45/1/10/{page}.json'.format(**url_params))

        req = self.session.get(url)
        res = req.json()
        assert type(res) == dict, print(type(res))
        msg = res['message']

        if msg == '成功':
            data = res['data']
            num = data['numFound']
            total_page = math.ceil(num / 10)
            items = data['item']

            # 取数据
            for item in items:
                spname = item['spname']
                min_score = item['min']
                avg = item['average']
                print(f'{spname:<20}\tmin: {min_score:<10}\tavg: {avg:<10}')
            else:
                # 当前数据取完后，要看看还有没有下一页
                if page < total_page:
                    page += 1
                    self.get_major_name(school_code, page)
        else:
            print('没有数据')
            print(res)

    
if __name__ == '__main__':

    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/91.0.4472.124 Safari/537.36'),
        'Connection': 'keep-alive'
    }
    args = sys.argv
    code = args[1]
    pm = parseMajor()
    pm.update_headers(headers)
    pm.get_major_name(code)

