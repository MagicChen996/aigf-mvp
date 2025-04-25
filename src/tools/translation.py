import requests
import random
import json
from hashlib import md5
from settings import BAIDU_APPID, BAIDU_APPKEY
class BaiDuTransTool:
    def __init__(self):
        self.appid = BAIDU_APPID
        self.appkey = BAIDU_APPKEY
        self.url = 'http://api.fanyi.baidu.com' + '/api/trans/vip/translate'
    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def trans_zh_to_en(self, query):
        from_lang = 'zh'
        to_lang =  'en'
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.appid + query + str(salt) + self.appkey)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()
        return result["trans_result"][0]['dst']