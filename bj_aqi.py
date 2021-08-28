# -*- coding:utf-8 -*-

"""
代码主要作用：获取 AQI 数据
北京：https://www.iqair.cn/cn/china/beijing
亦庄：https://www.iqair.cn/cn/china/beijing/yizhuang-bda
大兴：https://www.iqair.cn/cn/china/beijing/daxing
通州：https://www.iqair.cn/cn/china/beijing/tongzhou
丰台云岗：https://www.iqair.cn/cn/china/beijing/fengtai-yungang
丰台小屯：https://www.iqair.cn/cn/china/beijing/fengtai-xiaotun
"""

import re
import requests
from odps import ODPS

o = ODPS('', '', '', '')
args = {'gmtdate': ''}


class Iqair:

    def __init__(self):
        self.session = requests.Session()

    def update_header(self, headers):
        self.session.headers.update(headers)

    def send_request(self, url):
        req = self.session.get(url)
        res = req.content.decode('utf-8')

        return res

    def parse_detail(self, response, city):
        """使用正则解析 HTML，并返回解析后的结果列表"""

        ret = []
        # 取更新时间
        update_time = re.search('<time .+?>(.+?)</time>', response).group(1)

        # 先解析等级部分信息
        table = re.search(
            'class="aqi-overview-detail__main-pollution-table".+?</table>',
            response, re.S).group()
        attr_tag = re.search('<thead(.+?)>', table).group(1)
        level_info = re.findall('td' + attr_tag + '>(.+?)</td>', table)
        level = level_info[0].strip()
        aqi_index = level_info[1].split(' ')[1]

        ret.append((city, 'level', level, ''))
        ret.append((city, 'aqi', aqi_index, ''))
        ret.append((city, 'updateTime', update_time, ''))

        # 再解析详细的污染物信息
        table2 = re.search(
            'class="aqi-overview-detail__other-pollution-table".+?</table>',
            response, re.S).group()
        trs = re.findall('tr' + attr_tag + '>(.+?)</tr>', table2)
        for tr in trs[1:]:
            ret_list = re.findall('td' + attr_tag + '>(.+?)</td>', tr)
            name = ret_list[0].strip()
            idx = ret_list[2].split(' ')[1]
            unit = re.search('class="unit">(.+?)</span>', ret_list[2]).group(1)
            ret.append((city, name, idx, unit.encode('utf-8')))

        return ret

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
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36}')
    }

    pre_dict = {
        'dx': {
            'point': [
                {
                    'name': '大兴区',
                    'url': 'https://www.iqair.cn/cn/china/beijing/daxing'
                }
            ]
        },
        'bj': {
            'point': [
                {
                    'name': '北京市',
                    'url': 'https://www.iqair.cn/cn/china/beijing'
                }
            ]
        },
        'ft': {
            'point': [
                {
                    'name': '丰台小屯',
                    'url': 'https://www.iqair.cn/cn/china/beijing/fengtai-xiaotun'
                },
                {
                    'name': '丰台云岗',
                    'url': 'https://www.iqair.cn/cn/china/beijing/fengtai-yungang'
                }
            ]

        },
        'tz': {
            'point': [
                {
                    'name': '通州区',
                    'url': 'https://www.iqair.cn/cn/china/beijing/tongzhou'
                }
            ]
        },
        'yz': {
            'point': [
                {
                    'name': '亦庄开发区',
                    'url': 'https://www.iqair.cn/cn/china/beijing/yizhuang-bda'
                }
            ]
        }
    }

    table_name = 'stg_kqzl_aqi_df'
    pt_str = 'dt=' + args['gmtdate']
    iqair = Iqair()
    iqair.update_header(headers)
    data = []
    for city in pre_dict:
        points = pre_dict[city]['point']
        for point in points:
            url = point['url']
            res = iqair.send_request(url)
            aqi = iqair.parse_detail(res, city)
            if aqi:
                print(aqi)
                data.extend(aqi)
    else:
        print(data)
    #     iqair.drop_partition(table_name, pt_str)
    #     iqair.write2odps(data, table_name, pt_str, project='sjzt_stg')


if __name__ == '__main__':
    run()
