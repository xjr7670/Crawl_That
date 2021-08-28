## 1. ����˵��

### ��������

* ���ԣ� Python3.7
* ��������������requests
* ���磺������

### ������Դ

����Ԥ��������Դ�Ա������������վ [http://bj.cma.gov.cn/](http://bj.cma.gov.cn/)

������Դ��

* ����������Ԥ����[http://bj.cma.gov.cn/qxfw/yjxx/bjs/](http://bj.cma.gov.cn/qxfw/yjxx/bjs/)
* ����������Ԥ����[http://bj.cma.gov.cn/qxfw/yjxx/dxq/](http://bj.cma.gov.cn/qxfw/yjxx/dxq/)


����ͼ��ͨ�����������������ӣ�ҳ�棩��ץȡ��ͼ��ʾ���ֵ����ݡ�<br>
�������⡢���С��ź����͡��źż��𡢷���ʱ�䡢�������ݡ�������

![img_2.png](img_2.png)

## 2. �����߼�

ͨ�����ҳ�� HTTP ���󣬿���ȷ��������ҳ���е����ݶ���Դ�����µĻص���

�����У�http://101.200.145.109:8087/weather/scene/warningPage.do?callback=cb6&pageNo=1&doc=������&_=1629168887578
��������http://101.200.145.109:8087/weather/scene/warningPage.do?callback=cb6&pageNo=1&doc=������&_=1629171491467

�������ӵ���Ӧʾ����

```json
cb6({"current":"1","total":34,"value":[{"channelname":"������","cttime":"2021-08-17 06:30:00","id":10540,"title":"����������׵���ɫԤ��"},{"channelname":"������","cttime":"2021-08-17 01:35:00","id":10528,"title":"��������������ɫԤ��"},{"channelname":"������","cttime":"2021-08-16 22:35:00","id":10509,"title":"��������������ɫԤ��"},{"channelname":"������","cttime":"2021-08-16 21:50:00","id":10503,"title":"���������������ɫԤ��"},{"channelname":"������","cttime":"2021-08-16 21:25:00","id":10497,"title":"����������������ɫԤ��"},{"channelname":"������","cttime":"2021-08-16 21:25:00","id":10499,"title":"���������������ɫԤ��"},{"channelname":"������","cttime":"2021-08-16 20:00:00","id":10471,"title":"�����������׵���ɫԤ��"},{"channelname":"������","cttime":"2021-08-16 07:05:00","id":10447,"title":"����������׵��ɫԤ��"},{"channelname":"������","cttime":"2021-08-15 14:40:00","id":10423,"title":"�����������׵��ɫԤ��"},{"channelname":"������","cttime":"2021-08-15 08:50:00","id":10403,"title":"����������׵��ɫԤ��"},{"channelname":"������","cttime":"2021-08-14 19:50:00","id":10348,"title":"�����������׵��ɫԤ��"},{"channelname":"������","cttime":"2021-08-14 08:50:00","id":10325,"title":"�����������׵���ɫԤ��"},{"channelname":"������","cttime":"2021-08-13 23:20:00","id":10308,"title":"�����������׵���ɫԤ��"},{"channelname":"������","cttime":"2021-08-12 18:45:00","id":10275,"title":"����������׵���ɫԤ��"},{"channelname":"������","cttime":"2021-08-12 07:30:00","id":10258,"title":"�����������׵���ɫԤ��"}]})
```

������ҳ���п��Եõ��������Ԥ����Ϣ�� id������� id ���뵽�����������ٷ�����������Եõ�Ԥ����������Ϣ��

������Ԥ�����飺http://101.200.145.109:8087/weather/scene/warningbyid.do?callback=cb6&doc={id}&_=1629187438276
������Ԥ�����飺http://101.200.145.109:8087/weather/scene/warningbyid.do?callback=cb6&doc={id}&_=1629187258213

Ԥ��������Ӧʾ����

```json
cb6({"channelname":"������","cttime":"2021-08-17 06:30:00","id":10540,"mainbody":"{\"city\":\"�����д�����\",\"image\":\"leidianlanse\",\"pubbody\":\"Ŀǰ��Ӱ������������������Ѽ����Ƴ�������׵���ɫԤ���źš�\",\"pubtime\":\"2021-08-17 06:30:00\",\"pubuser\":\"��־��\",\"signclass\":\"�׵�\",\"signrank\":\"��ɫ\",\"title\":\"����������׵���ɫԤ��\"}","title":"����������׵���ɫԤ��"})
```

ͨ���򵥵��ַ����������Խ�����������Ӧ���ݴ���ɱ�׼�� json ��ʽ�ٽ��н���������ȡ����Ӧ������

�����м���������Ԥ�����ݶ���ͬ���ķ�ʽ��ȡ��������⡣


## 3. ����˵��

�������������£�

```python
class WeatherWarning:
    def __init__(self):
        pass
    def update_header(self, headers):
        pass
    def send_request(self, url):
        pass
    def get_id(self, response):
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
��ʵ�������� `WeatherWarning` �������෽�����λ�ȡԤ�� ID������Ԥ�� ID ��ȡԤ�����顢ɾ����������з������ѽ��д�뵽 MaxCompute ��

### WeatherWarning ��˵��

#### __init__

��ʼ����������ȡ HTTP �Ự����ͬһ�����У���������ˣ�������ʱʹ��ͬһ���Ự

#### update_header

��������ͷ��Ϊ��ģ����ʵ�������

#### send_request

���� HTTP ���󣬷�����Ӧ�������ġ�������ȡ ID ����ȡԤ�����������ͨ���������ʵ��

#### get_id

��ȡԤ�� ID������ ID �б�

#### parse_detail

����Ԥ��������Ϣ��������Ԥ����Ϣ������������ɵ��б�

#### drop_partition

ɾ���������еķ�������Ϊ MaxCompute �� python sdk ���ṩ������ sql �е� `insert overwrite` ������ֻ����ɾ��ԭ�з�����д���Դﵽ���Ǹ���

#### write2odps

���������д�뵽 MaxCompute ����

## 4. ����

����Ŀǰλ�� **sjzt_stg** ��Ŀ�£�ҵ�����̣���ׯ���д��� -> MaxCompute -> ���ݿ��� -> weather_warning.py

ÿ 1 Сʱִ��һ��
