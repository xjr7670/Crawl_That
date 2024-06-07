# -*- coding:utf-8 -*-

import sys
import json
import time
import requests


class UpdateM1M2:
    def __init__(self, lmt=None):
        self.month_limit = lmt

    @staticmethod
    def get_data():

        url = 'https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0D01%22%7D%5D&k1={ts}&h=1'.format(ts=round(time.time()*1000))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'pplication/json, text/javascript, */*; q=0.01'
        }

        req = requests.get(url, headers=headers)    
        data = {}
        data= req.json()
        # with open('/mnt/e/temp/easyquery.txt', encoding='utf8') as f:
        #     data = json.loads(f.read())

        return data

    def parse_data(self, json_data):

        # M2       - A0D0101
        # M2同比   - A0D0102
        # M1       - A0D0103
        # M1同比   - A0D0104
        # 现金     - A0D0105
        # 现金同比 - A0D0106

        returncode = json_data['returncode']
        datanodes = json_data['returndata']['datanodes']

        def sorted_data(code):
            ret = [item for item in datanodes if item['code'][3:10] == code]
            sorted(ret, key=lambda item: item['code'])

            return ret

        def combine_data(data_code, rate_code, lm):
            data_metric = [
                (item['wds'][1]['valuecode'], item['data']['data']) for item in sorted_data(data_code) 
                if item['data']['hasdata'] and item['wds'][0]['valuecode'] == data_code
            ][0:lm]
            rate_metric = [
                (item['wds'][1]['valuecode'], item['data']['data']) for item in sorted_data(rate_code)
                if item['data']['hasdata'] and item['wds'][0]['valuecode'] == rate_code
            ][0:lm]
            ret = {}

            for i in range(lm):
                mon = data_metric[i][0]
                ret[mon] = (data_metric[i][1], rate_metric[i][1])

            return ret

        if self.month_limit:
            if self.month_limit > 12:
                his_cnt = 12
            else:
                his_cnt = self.month_limit
        else:
            his_cnt = 5
        m1_data = combine_data('A0D0101', 'A0D0102', his_cnt)
        m2_data = combine_data('A0D0103', 'A0D0104', his_cnt)
        cash_data = combine_data('A0D0105', 'A0D0106', his_cnt)

        return [m1_data, m2_data, cash_data]

    @staticmethod
    def print_result(dict_list):  
        title = ['M2', 'M1', 'CASH']
        for metric, t in zip(dict_list, title):
            print('\n{:4} - \n\t{:8}\t|\t{:10}\t|\t{:4}\t|\t{:4}'.format(t, 'month', 'value', 'YoY', 'MoM'))
            print('\t', '-'*66)
            last_month = None
            for mon, data in metric.items():
                value = data[0]
                if last_month:
                    mom = round((value-last_month)*100/last_month, 1)
                else:
                    mom = '-'
                    last_month = value
                print('\t{:10s}\t|\t{:<10}\t|\t{:>4}\t|\t{:>4}'.format(mon, value, data[1], mom))

    def run(self):
        json_data = self.get_data()
        data = self.parse_data(json_data)
        self.print_result(data)        

if __name__ == '__main__':

    args = sys.argv
    lm = None
    if len(args) >= 2:
        lm = int(args[1])
    uobj = UpdateM1M2(lm)
    uobj.run()

