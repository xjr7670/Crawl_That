# -*- coding:utf-8 -*-

"""
代码主要作用：
"""

import re
import time
import datetime
import requests


class WeatherForcast:

    def __init__(self):
        self.session = requests.Session()

    def update_header(self, headers):
        self.session.headers.update(headers)

    def send_request(self, url):
        req = self.session.get(url)
        res = req.content.decode('utf-8')

        return res

    def parse_7d(self, response):
        """使用正则解析 HTML，并返回解析后的结果列表"""
        ret = []

        parse_time = round(time.time())
        update_time = re.search('id="update_time" value="(.*?)"',
                                response, re.S)
        update_time = update_time.group(1)
        ul = re.search('<ul class="t clearfix">.*?</ul>', response, re.S)
        ul = ul.group().replace('\n', '')
        lis = re.findall('<li.*?</li>', ul)
        l_tem = h_tem = ''
        wind_name1 = wind_code1 = ''
        wind_name2 = wind_code2 = ''
        for li in lis:
            day = re.search('(\d{1,2})日', li).group(1)
            wea = re.search('class="wea">(.*?)</p>', li).group(1)
            tem = re.search('class="tem">(.*?)</p>', li).group(1)
            tem = re.findall('\d{1,2}', tem)
            if len(tem) == 2:
                h_tem, l_tem = tem
            elif len(tem) == 1:
                h_tem = l_tem = wea[0]
            wind = re.search('p class="win">(.*?)</p>', li).group(1)
            wind_direction = re.findall('title="(.*?)" class="(.*?)"', wind)
            if len(wind_direction) == 2:
                wind_name1, wind_code1 = wind_direction[0]
                wind_name2, wind_code2 = wind_direction[1]
            elif len(wind_direction) == 1:
                wind_name1, wind_code1 = wind_direction[0]
                wind_name2 = wind_code2 = ''
            wind_level = re.search('<i>(.*?)</i>', wind).group(1)
            ret.append([
                day, wea, l_tem, h_tem, wind_name1, wind_code1,
                wind_name2, wind_code2, wind_level, update_time,
                parse_time
            ])

        return ret

    def parse_15d(self, response):
        """解析15天的页面HTML"""

        ret = []
        update_time = re.search('id="update_time" value="(.*?)"',
                                response, re.S)
        update_time = update_time.group(1)
        parse_time = round(time.time())
        ul = re.search('<ul class="t clearfix">(.*?)</ul>', response,
                       re.S).group(1)
        ul = ul.replace('\n', '')
        lis = re.findall('<li.*?</li>', ul)
        h_tem = l_tem = None
        for li in lis:
            day = re.search('class="time">(.+?)</span>', li).group(1)
            day = re.search('\d{1,2}', day).group()
            wea = re.search('class="wea">(.*?)</span>', li).group(1)
            tem = re.search('class="tem">(.*?)</span>', li).group(1)
            tem = re.findall('\d{1,2}', tem)
            if len(tem) == 2:
                h_tem, l_tem = tem
            elif len(tem) == 1:
                h_tem = l_tem = tem[0]
            wind_direction = re.search('class="wind">(.*?)</span>', li).group(1)
            wind_level = re.search('class="wind1">(.*?)</span>', li).group(1)
            ret.append([
                day, wea, l_tem, h_tem, wind_direction, '',
                '', '', wind_level, update_time, parse_time
            ])
        return ret

    def parse_html(self, response, date_range):
        """解析方法的统一入口，根据 date_range 判断选择使用哪一个方法"""

        data = None
        if date_range == 7:
            data = self.parse_7d(response)
        elif date_range == 15:
            data = self.parse_15d(response)

        return data

    def drop_partition(self, tb_name, pt_str, project='sjzt_stg'):
        """每次更新数据前，先删除历史数据"""
        t = o.get_table(tb_name, project=project)
        t.delete_partition(pt_str, if_exists=True)

    def write2odps(self, data, tb_name, pt_str, project='sjzt_stg'):
        """写数据到 MaxCompute """
        t = o.get_table(tb_name, project=project)
        with t.open_writer(partition=pt_str, create_partition=True) as writer:
            writer.write(data)
        print(f'已写入 {len(data)} 条数据到 {project}.{tb_name}')


def run():
    """入口函数"""

    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                       ' (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36}'),
        'Host': 'www.weather.com.cn'
    }
    url_temp_str = 'http://www.weather.com.cn/{day}/{code}.shtml'
    city_code = ['101010100', '101011100']
    dates = [7, 15]
    param_dict = {
        7: 'weather',
        15: 'weather15d'
    }
    tables = {
        '101010100': 'stg_bjtq_15d_df',  # 保存北京市的天气预报数据
        '101011100': 'stg_dxtq_15d_df'  # 保存大兴区的天气预报数据
    }

    pt_str = 'dt=' + datetime.datetime.today().strftime('%Y%m%d')
    wf = WeatherForcast()
    wf.update_header(headers)

    for code in city_code:
        table_name = tables[code]
        wf.drop_partition(table_name, pt_str)
        for d in dates:
            url = url_temp_str.format(day=param_dict[d],
                                      code=code)
            print('url: ', url)
            response = wf.send_request(url)
            data = wf.parse_html(response, d)
            print(data)
            wf.write2odps(data, table_name, pt_str, project='sjzt_stg')


if __name__ == '__main__':
    run()
