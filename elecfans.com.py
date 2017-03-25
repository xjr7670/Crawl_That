'''

模拟登录elecfans.com这个网站

用到的第三方库是requests

除了用户名和密码外，还需要获取到初次登录后返回的syncurl里面的值，其中包含有一系列的URL。依次请求这些URL（估计是验证用）后，才算是最终登录成功

完成时间：2017年3月25日
'''

import json
import requests

data = {
    'referer': 'http://bbs.elecfans.com/home.php?mod=spacecp',
    'siteid': 4,
    'account': username,
    'password': password
    }

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'no-cache',
    'Content-Length': 121,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'passport.elecfans.com',
    'Origin': 'http://passport.elecfans.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://passport.elecfans.com/login?infloat=yes&referer=http%3A%2F%2Fbbs.elecfans.com%2Fhome.php%3Fmod%3Dspacecp&siteid=4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

session = requests.Session()
login_res = session.post('http://passport.elecfans.com/login/dologin.html', data=data, headers=headers)
login_res_json = json.loads(login_res.text)

url_list = login_res_json['data']['syncurl']
for url in url_list:
    session.get(url)

res = session.get('http://bbs.elecfans.com/home.php?mod=spacecp')
html = res.content.decode()
print(html)
