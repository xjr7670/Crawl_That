# -*- coding:utf-8 -*-

"""
代码主要作用：从北京气象局网站（http://bj.cma.gov.cn/qxfw/yjxx/bjs/）抓取气象预警信息
"""

import json
import time
import requests


class WeatherWarning:

    def __init__(self):
        self.session = requests.Session()

    def update_header(self, headers):
        self.session.headers.update(headers)

    def send_request(self, url):
        req = self.session.get(url)
        res = req.content.decode('utf-8')

        return res

    def get_id(self, response):
        """针对列表请求所返回的内容进行解析，判断是否有当天的预警内容，如果有则返回预警的 ID 列表"""

        json_str = response[4:-1]
        list_object = json.loads(json_str)
        warn_list = list_object['value']
        today = args['today']
        ret = []
        for item in warn_list:
            cttime = item['cttime']
            day = cttime.split(' ')[0]
            if day == today:
                ret.append(item['id'])

        return ret

    def parse_detail(self, response):
        """使用正则解析 HTML，并返回解析后的结果列表"""

        json_str = response[4:-1]
        object = json.loads(json_str)
        mainbody = json.loads(object['mainbody'])
        title = mainbody['title']
        city = object['channelname']
        pubtime = mainbody['pubtime']
        signclass = mainbody['signclass']
        signrank = mainbody['signrank']
        pubbody = mainbody['pubbody']
        pubuser = mainbody['pubuser']

        parse_time = round(time.time())

        ret = [title, city, signclass, signrank, pubtime,
               pubbody, pubuser, parse_time]

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
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                       ' (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36}')
    }

    pre_dict = {
        'dx': {
            'warn_list_url': 'http://101.200.145.109:8087/weather/scene/warningPage.do?callback=cb6&pageNo=1&doc=大兴区&_=1629171491467',
            'warn_detail_url': 'http://101.200.145.109:8087/weather/scene/warningbyid.do?callback=cb6&doc={id}&_=1629187258213',
            'stg_table': 'stg_qxyj_dx_df'
        },
        'bj': {
            'warn_list_url': 'http://101.200.145.109:8087/weather/scene/warningPage.do?callback=cb6&pageNo=1&doc=北京市&_=1629168887578',
            'warn_detail_url': 'http://101.200.145.109:8087/weather/scene/warningbyid.do?callback=cb6&doc={id}&_=1629187438276',
            'stg_table': 'stg_qxyj_bj_df'
        }
    }

    pt_str = 'dt=' + args['gmtdate']
    ww = WeatherWarning()
    ww.update_header(headers)
    citys = ['bj', 'dx']
    for city in citys:
        list_url = pre_dict[city]['warn_list_url']
        detail_url = pre_dict[city]['warn_detail_url']
        table_name = pre_dict[city]['stg_table']
        res = ww.send_request(list_url)
        id_list = ww.get_id(res)
        data = []
        if id_list:
            for id_ in id_list:
                url = detail_url.format(id=id_)
                detail_res = ww.send_request(url)
                ret = ww.parse_detail(detail_res)
                print(ret)
                data.append(ret)
            else:
                ww.drop_partition(table_name, pt_str)
                ww.write2odps(data, table_name, pt_str, project='sjzt_stg')


if __name__ == '__main__':
    run()
