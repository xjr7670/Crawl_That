#-*- coding:utf-8 -*-

"""
读取 Redis 中的章节标题与内容，写入到 mongodb 中
"""

import time
import redis
import pymongo


class Redis2Mongo(object):

    def __init__(self, redis_conf, mongo_conf):
        self.redis_conf = redis_conf
        self.mongo_conf = mongo_conf
        self.redis_pool = self.get_redis_pool(self.redis_conf)

    def get_redis_pool(self, redis_conf, db=None):
        """获取 redis 连接池"""

        pool = redis.ConnectionPool(host=redis_conf['host'], 
                                    port=redis_conf['port'],
                                    password=redis_conf.get('password', ''),
                                    db=db if db else redis_conf.get('db', 0))
        return pool

    def get_mongo_handler(self, mongo_conf=None):
        """获取 mongodb 句柄"""

        if not mongo_conf:
            mongo_conf = self.mongo_conf
        client = pymongo.MongoClient(mongo_conf['uri'])
        db = client.get_database(mongo_conf['db'])
        collection = db.get_collection(mongo_conf['collection'])
        return collection

    def write_to_mongodb(self, result_list: list):
        """"写入到 mongodb """
        
        mongo_handler = self.get_mongo_handler()
        _ = mongo_handler.insert_many([{'title': t, 'content': c}
                                       for t, c in result_list])

    def run(self):
        """从 redis 中读取数据，然后写入到 mongodb"""
        
        result_set = []
        r = redis.Redis(connection_pool=self.redis_pool)
        title = r.lpop('title')
        title = title.decode() if title else None
        content = r.lpop('content')
        content = content.decode() if content else None
        total_write = 0
        freq = 500
        sleep_seconds = 1 * 60
        void_print = True
        while True:
            if title:
                result_set.append((title, content))
                void_print = True
            else:
                if result_set:
                    self.write_to_mongodb(result_set)
                    total_write += len(result_set)
                    result_set.clear()
                    print('共已写入 %d 条数据到 mongodb' % total_write)
                void = True
            
                if void and void_print:
                    print('Redis 中已经没有数据，程序将暂停 %d 秒，'
                          '随时可按 Ctrl-C 终止运行...' % sleep_seconds)
                    void_print = False
                    time.sleep(sleep_seconds)
            title = r.lpop('title')
            title = title.decode() if title else None
            content = r.lpop('content')
            content = content.decode() if content else None
            if result_set and len(result_set) % freq == 0:
                # 每 500 条写入一次到 mongodb
                self.write_to_mongodb(result_set)
                total_write += freq
                result_set.clear()
                print('共已写入 %d 条数据到 mongodb' % total_write)


if __name__ == '__main__':

    # redis 配置
    redis_config = {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 1
    }
    # mongodb 配置
    mongo_config = {
        'uri': 'mongodb://study:studymongodb@122.51.39.219/student',
        'db': 'student',
        'collection': 'doupocangqiong_Content'
    }

    r2m = Redis2Mongo(redis_config, mongo_config)
    r2m.run()
