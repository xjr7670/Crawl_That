# -*- coding:utf-8 -*-

"""
代码主要作用：
"""
import datetime

import requests
from lxml import etree

class WeatherForcast:

    def __init__(self):
        self.session = requests.Session()

    def update_header(self, headers):
        self.session.headers.update(headers)

    def send_request(self, url):
        req = self.session.get(url)
        res = req.content.decode('utf-8')

        return res

    def parse_html(self, response):
        """解析 HTML，并返回解析后的结果列表"""
        root = etree.HTML(response)
        div = root.xpath('//div[@id="7d"]')[0]
        ulist = div.xpath('ul[@class="t clearfix"]/li')
        ret = []
        for u in ulist:
            date = u.xpath('h1/text()')[0]
            wea = u.xpath('p[@class="wea"]/text()')[0]
            l_tem = u.xpath('p[@class="tem"]/span/text()')
            if l_tem:
                l_tem = l_tem[0]
            else:
                l_tem = ''
            h_tem = u.xpath('p[@class="tem"]/i/text()')[0]
            wind = u.xpath('p[@class="win"]')[0]
            direction = wind.xpath('em/span')
            wind_direction1_name = direction[0].xpath('@title')[0]
            wind_direction1_code = direction[0].xpath('@class')[0]
            if len(direction) == 2:
                wind_direction2_name = direction[1].xpath('@title')[0]
                wind_direction2_code = direction[1].xpath('@class')[0]
            else:
                wind_direction2_name = wind_direction2_code = ''
            wind_force = wind.xpath('i/text()')[0]
            ret.append({
                'date': date,
                'weather': wea,
                'low_temp': l_tem,
                'hight_temp': h_tem,
                'wind_d_name1': wind_direction1_name,
                'wind_d_code1': wind_direction1_code,
                'wind_d_name2': wind_direction2_name,
                'wind_d_code2': wind_direction2_code,
                'wind_force': wind_force
            })
        print(ret)
        return ret

    def write2odps(self, data, tb_name, pt_str, project='sjzt_stg'):
        """写数据到 MaxCompute """
        t = o.get_table(tb_name, project=project)
        with t.open_writer(partition=pt_str) as writer:
            writer.write(data)


def run(date_range, city_code):
    """入口函数
    :date_range: 日期区别值，分别为 7 或 15。等于 7 时获取 1-7 天的数据。等于 15 时获取 8-15 天的数据
    :city_code: 城市代码
    """

    headers = {}
    wf = WeatherForcast()
    wf.update_header(headers)
    url_temp_str = 'http://www.weather.com.cn/{day}/{code}.shtml'
    param_dict = {
        7: 'weather',
        15: 'weather15d'
    }
    url = url_temp_str.format(day=param_dict[date_range],
                              code=city_code)

    response = wf.send_request(url)

    data = wf.parse_html(response)
    table_name = ''
    pt_str = 'dt=' + datetime.datetime.today().strftime('%Y%m%d')

    # wf.write2odps(data, pt_str)


if __name__ == '__main__':

    city_code = ['101010100', '101011100']
    dates = [7, 15]
    for code in city_code:
        for d in dates:
            run(d, code)
