## 1. ����˵��

### ��������

* ���ԣ� Python3.7
* ��������������requests
* ���磺������

### ������Դ

����Ԥ��������Դ���й������� [http://www.weather.com.cn/](http://www.weather.com.cn/)

������Դ��

* ����������[http://www.weather.com.cn/weather/101010100.shtml](http://www.weather.com.cn/weather/101010100.shtml)
* ����������[http://www.weather.com.cn/weather/101011100.shtml](http://www.weather.com.cn/weather/101011100.shtml)

����ͼ��ͨ�����������������ӣ�ҳ�棩��ץȡ��ͼ��ʾ���ֵ����ݡ�<br>
�����ӽ�����δ��14�죨��15�죩�����ڡ�Ԥ��������������¡�������¡����򡢷���������ʱ��

![img.png](img.png)

## 2. �����߼�

����ͨ������ҳ��� HTML ���룬ʹ��������ʽƥ��ķ�ʽ��Դ���л�ȡ����Ҫ�����ݡ�<br>
����ͼ��ʾ

![img_1.png](img_1.png)

7 ���Ԥ�����ݶ������� `class="t clearfix"` �� `ul` ��ǩ�ڡ�

* ���� `h1` ��ǩ���Ի�ȡ����ֵ
* ���� `class="wea"` ��ǩ����ȡ������Ԥ���ı�
* ���� `class="tem"` ��ǩ����ȡ��������¼������������
* ���� `class="win"` ��ǩ����ȡ�÷��򼰷�������

8-15 ���Ԥ�������߼����ƣ�����7�족����8-15�족�����ݺϲ���һ�𼴿ɵõ� 15 �������Ԥ�����ݡ�

����ʱ�������һ�� `id="update_time"` �����ر�ǩ�ڣ�
```html
<input type="hidden" id="update_time" value="07:30"/>
```

�����м���������Ԥ�����ݶ���ͬ���ķ�ʽ��ȡ��������⡣


## 3. ����˵��

�������������£�

```python
class WeatherForecast:
    def __init__(self):
        pass
    def update_header(self, headers):
        pass
    def parse_7d(self, response):
        pass
    def parse_15d(self, response):
        pass
    def parse_html(self, response, date_range):
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
��ʵ�������� `WeatherForcast` �������෽������ɾ����������з�������ȡҳ�� HTML ���롢���� HTML ���롢�ѽ��д�뵽 MaxCompute ��

### WeatherForecast ��˵��

#### __init__

��ʼ����������ȡ HTTP �Ự����ͬһ�����У���������ˣ�������ʱʹ��ͬһ���Ự

#### update_header

��������ͷ��Ϊ��ģ����ʵ�������

#### parse_7d

���� 7 ��� HTML ҳ����룬��ȡ��Ҫ������Ԥ������

#### parse_15d

���� 8-15 ��� HTML ҳ����룬��ȡ��Ҫ������Ԥ������

#### parse_html

������ 7 ��� 8-15 ��ĺ�������װ�����ݴ������ĵ�����ֵ�Զ�ѡ���Ӧ�ķ���

#### drop_partition

ɾ���������еķ�������Ϊ MaxCompute �� python sdk ���ṩ������ sql �е� `insert overwrite` ������ֻ����ɾ��ԭ�з�����д���Դﵽ���Ǹ���

#### write2odps

���������д�뵽 MaxCompute ����

## 4. ����

����Ŀǰλ�� **sjzt_stg** ��Ŀ�£�ҵ�����̣���ׯ���д��� -> MaxCompute -> ���ݿ��� -> weather_forecast.py

ÿ 30 ����ִ��һ��
