## 1. ����˵��

### ��������

* ���ԣ� Python3.7
* ��������������requests
* ���磺������

### ������Դ

����Ԥ��������Դ��IQAir��վ [https://www.iqair.cn/](https://www.iqair.cn/)

������Դ��

* ������https://www.iqair.cn/cn/china/beijing
* ��ׯ��https://www.iqair.cn/cn/china/beijing/yizhuang-bda
* ���ˣ�https://www.iqair.cn/cn/china/beijing/daxing
* ͨ�ݣ�https://www.iqair.cn/cn/china/beijing/tongzhou
* ��̨�Ƹڣ�https://www.iqair.cn/cn/china/beijing/fengtai-yungang
* ��̨С�ͣ�https://www.iqair.cn/cn/china/beijing/fengtai-xiaotun


����ͼ��ͨ�����������������ӣ�ҳ�棩��ץȡ��ͼ��ʾ���ֵ����ݡ�<br>
��������ʱ�䡢AQI��ֵ������ָ��������Ⱦ����ϸָ���

![img_3.png](img_3.png)

## 2. �����߼�

ǰ������ȫ������ҳ��� HTML Դ���У�����

* ����ʱ��λ�� `<time _ngcontent-airvisual-web-c158></time>` ��ǩ��
* AQI ָ��ֵΪ�� `<p _ngcontent-airvisual-web-c170="" class="aqi-value__value"></p>` ��ǩ��
* ����λ�� `<span _ngcontent-airvisual-web-c170="" class="aqi-status__text"></span>` ��ǩ��
* ��Ⱦ������λ�� `<table _ngcontent-airvisual-web-c170="" class="aqi-overview-detail__other-pollution-table"></table>` ��ǩ��

���������� `_ngcontent-airvisual-web-c170` ���Կ����ڲ�ͬ��ҳ�治ͬ����˴����߼�������ȡ���ֵ���������ֵȥ������ƥ�䣨ɸѡ����

ͨ��������ʽһ������С��Χ������ȡ����Ҫ�����ݡ��������붼������һ�ű��У�`sjzt_stg.stg_kqzl_aqi_df`


## 3. ����˵��

�������������£�

```python
class Iqair:
    def __init__(self):
        pass
    def update_header(self, headers):
        pass
    def send_request(self, url):
        pass
    def parse_detail(self, response):
        pass
    def drop_partition(self, tb_name, pt_str, project='sjzt_stg'):
        pass
    def write2odps(self, data, tb_name, pt_str, project='sjzt_stg'):
        pass

def run():
    pass

if __name__ == '__main__':
    run()
```

���������µ� `run()` ��ʼ�����뵽 `def run()` �ڲ���
`run()` ���������� HTTP ����ͷ��URL�����������������
��ʵ�������� `Iqair` ��ѭ������������Ҫץȡ���ݵĵ�ַ��������Ϊ5�������������󡢽���ҳ��õ����ݣ�ɾ����������з������ѽ��д�뵽 MaxCompute ��

### Iqair ��˵��

#### __init__

��ʼ����������ȡ HTTP �Ự���󣬷��Ͳ�ͬ����������ʱʹ��ͬһ���Ự

#### update_header

��������ͷ��Ϊ��ģ����ʵ�����׼��

#### send_request

���� HTTP ���󣬷�����Ӧ�������ġ�

#### parse_detail

���� HTML Դ�룬ͨ��������ʽ����ƥ��

#### drop_partition

ɾ���������еķ�������Ϊ MaxCompute �� python sdk ���ṩ������ sql �е� `insert overwrite` ������ֻ����ɾ��ԭ�з�����д���Դﵽ���Ǹ���

#### write2odps

���������д�뵽 MaxCompute ����

## 4. ����

����Ŀǰλ�� **sjzt_stg** ��Ŀ�£�ҵ�����̣���ׯ���д��� -> MaxCompute -> ���ݿ��� -> weather_warning.py

ÿ 1 Сʱִ��һ��
