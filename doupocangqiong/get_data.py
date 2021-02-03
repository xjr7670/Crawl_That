#-*- coding:utf-8 -*-

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from lxml import etree
from lxml.html import tostring
import html
import requests
import redis
import pymongo


class MakeRequest(object):

    def __init__(self, url: str, conf: dict, headers: dict):
        self.target_url = url
        self.redis_conf = conf
        self.remove_html_pat = re.compile(r'<[^>]+>')
        self.remove_blank_pat = re.compile(r'\s')
        self.redis_pool = self.get_redis_pool(self.redis_conf)
        self.redis_content_pool = self.get_redis_pool(self.redis_conf, 1)
        self.redis_chapter_urls_key = 'chapter_urls'    # Redis 保存章节 URL 的 LIST 的名字
        self.session = self.get_http_session(headers)

    def get_redis_pool(self, redis_conf, db=None):
        """获取 redis 连接池"""

        pool = redis.ConnectionPool(host=redis_conf['host'], 
                                    port=redis_conf['port'],
                                    password=redis_conf.get('password', ''),
                                    db=db if db else redis_conf.get('db', 0))
        return pool

    def get_http_session(self, headers: dict):
        """获取 HTTP 会话"""

        session = requests.Session()
        session.headers.update(headers)

        return session

    def get_chapter_urls(self):
        """获取章节URL"""

        res = self.session.get(self.target_url)
        if res.status_code != 200 and res.status_code != 201:
            raise ConnectionError('Cannot open the website')

        src = res.content.decode('utf-8')
        root = etree.HTML(src)
        # 解析小说书名及作者、小说简介
        name = root.xpath('//div[@class="catalog"]/h1/text()')[0]
        author = root.xpath('//div[@class="info"]/a[2]/text()')[0]
        desc = root.xpath('//div[@class="summary"]/div[@class="intro"]/p/text()')[0]
        # 解析小说各章节 URL
        mulu_div = root.xpath('//div[@class="mulu-list"]')[0]
        chapter_urls = mulu_div.xpath('//li/a/@href')
        chapter_titles = mulu_div.xpath('//li/a/text()')

        return name, author, desc, chapter_titles, chapter_urls
    
    def put_url_to_redis(self, url_list):
        """把 URL 地址列表放到 redis 中"""

        r = redis.Redis(connection_pool=self.redis_pool)
        # 先清空
        _ = r.delete(self.redis_chapter_urls_key)
        count = r.lpush(self.redis_chapter_urls_key, *url_list)
        print('已将 {} 条 URL 添加到 Redis 中'.format(count))

    def get_chapter_content(self, chapter_url):
        """获取章节正文"""

        print('正在获取: ', chapter_url)
        res = self.session.get(chapter_url)
        status_code = res.status_code
        if status_code != 200 and status_code != 201:
            # 因为多线程会忽略异常，所以这里不抛出异常，直接打印出提示信息
            print('Cannot open: %s\tstatus code: %s' % (chapter_url,
                                                        status_code))
        src = res.content.decode('utf-8')
        title, content = self.parse_content(src)
        return title, content
    
    def parse_content(self, resp):
        """解析章节页面内容"""

        root = etree.HTML(resp)
        title = root.xpath('//div[@class="content book-content"]/h1/text()')[0]
        content_div = root.xpath('//div[@class="neirong"]')[0]
        # 获取章节正文，并去除多余的 HTML 标签以及空白
        content = html.unescape(tostring(content_div).decode())
        content = self.remove_html_pat.sub('', content)
        content = self.remove_blank_pat.sub('', content)

        return title, content

    def save_chapter_to_redis(self, title, content):
        """保存章节标题与内容到 Redis"""

        r = redis.Redis(connection_pool=self.redis_content_pool)
        _ = r.lpush('title', title)
        _ = r.lpush('content', content)

    def get_novel_data(self, target_url_list):
        """多线程获取小说数据"""

        url_len = len(target_url_list)
        with ThreadPoolExecutor(max_workers=url_len) as executor:
            futures = {executor.submit(self.get_chapter_content, url): 
                           url for url in target_url_list}
            for future in as_completed(futures):
                url = futures[future]
                print('%s 已完成。' % url)
                title, content = future.result()
                # 执行保存标题与正文的操作
                self.save_chapter_to_redis(title, content)
    
    def get_novel_data_to_redis(self, count=10):
        """获取小说数据的主函数"""

        r = redis.Redis(connection_pool=self.redis_pool)
        url_len = r.llen(self.redis_chapter_urls_key)
        start = 0
        end = count - 1
        while start < url_len:
            # 分批使用多线程获取
            url_list = r.lrange(self.redis_chapter_urls_key, start, end)
            self.get_novel_data(url_list)
            start += count
            end += count
        else:
            print('小说数据已完全写入到 Redis')

    @staticmethod
    def write_to_mongodb(mongo_conf, json_data, many=False):
        """把数据写入到 mongodb 中
        
        这里主要是写名字、作者、简介。以及章节 URL 与章节标题
        """

        client = pymongo.MongoClient(mongo_conf['uri'])
        db = client.get_database(mongo_conf['db'])
        collection = db.get_collection(mongo_conf['collection'])
        if many:
            _ = collection.insert_many(json_data)
        else:
            _ = collection.insert_one(json_data)
    
    def run(self, mongo_conf):
        """项目主入口"""

        # 获取小说名字、作者、简介以及所有章节的 URL
        name, author, desc, chapter_titles, chapter_urls \
            = self.get_chapter_urls()
        # 写入名字、作者、简单、章节 URL 与章节标题到 mongodb
        novel_name = mongo_conf['collection']
        mongo_conf['collection'] = novel_name + '_Describe_Author'
        self.write_to_mongodb(mongo_conf, {'NovelName': name,
                                           'Describe': desc,
                                           'Author': author})
        mongo_conf['collection'] = novel_name + '_Chapter'
        chapter_data = [{'title': t, 'url': url}
                        for t, url in zip(chapter_titles, chapter_urls)]
        self.write_to_mongodb(mongo_conf, chapter_data, many=True)
        # 把章节 URL 单独放到 redis 中
        self.put_url_to_redis(chapter_urls)
        # 根据章节 URL 获取到章节的标题与正文，并放入到 redis 中
        self.get_novel_data_to_redis()


if __name__ == '__main__':

    # 目标小说页
    url = 'https://www.51shucheng.net/wangluo/doupocangqiong'
    # redis 配置
    redis_config = {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0
    }
    # mongodb 配置
    mongo_config = {
        'uri': 'mongodb://study:studymongodb@122.51.39.219/student',
        'db': 'student',
        'collection': 'doupocangqiong'
    }
    # 请求头
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/79.0.3945.79 Safari/537.36'),
        'Accept': ('text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,image/webp,image/apng,*/*;'
                   'q=0.8,application/signed-exchange;v=b3;q=0.9')
    }
    mr = MakeRequest(url, redis_config, headers)
    mr.run(mongo_config)
