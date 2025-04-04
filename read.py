import os
import json
import requests
import time
import hashlib
import urllib.parse
import random

# 加密盐及其它默认值
KEY = "3c5c8717f3daf09iop3423zafeqoi"
READ_URL = "https://weread.qq.com/web/book/read"
RENEW_URL = "https://weread.qq.com/web/login/renewal"
COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}

referer_url = "https://weread.qq.com/web/reader/"
# github action部署用
# 从环境变量获取 headers、cookies等值(如果不存在使用默认本地值)
# 每一次代表30秒，比如你想刷1个小时这里填120，你只需要签到这里填2次

env_num = os.getenv('READ_NUM')

# headers = json.loads(json.dumps(eval(env_headers))
#                      ) if env_headers else local_headers
# cookies = json.loads(json.dumps(eval(env_cookies))
#                      ) if env_cookies else local_cookies
number = int(env_num) if env_num not in (None, '') else 120


def encode_data(data):
    return '&'.join(f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys()))


def cal_hash(input_string):
    _7032f5 = 0x15051505
    _cc1055 = _7032f5
    length = len(input_string)
    _19094e = length - 1

    while _19094e > 0:
        _7032f5 = 0x7fffffff & (_7032f5 ^ ord(
            input_string[_19094e]) << (length - _19094e) % 30)
        _cc1055 = 0x7fffffff & (_cc1055 ^ ord(
            input_string[_19094e - 1]) << _19094e % 30)
        _19094e -= 2

    return hex(_7032f5 + _cc1055)[2:].lower()


def get_wr_skey(headers, cookies):
    response = requests.post(RENEW_URL, headers=headers, cookies=cookies,
                             data=json.dumps(COOKIE_DATA, separators=(',', ':')))
    for cookie in response.headers.get('Set-Cookie', '').split(';'):
        if "wr_skey" in cookie:
            return cookie.split('=')[-1][:8]
    return None


def read(headers, cookies, data, userid):
    index = 1
    headers['referer'] = referer_url + data['b']
    while index <= number:
        data['ct'] = int(time.time())
        data['ts'] = int(time.time() * 1000)
        data['rn'] = random.randint(0, 1000)
        data['sg'] = hashlib.sha256(
            f"{data['ts']}{data['rn']}{KEY}".encode()).hexdigest()
        data['s'] = cal_hash(encode_data(data))
        print(f"\n用户{userid+1} 尝试第 {index} 次阅读...")
        response = requests.post(READ_URL, headers=headers, cookies=cookies, data=json.dumps(
            data, separators=(',', ':')))
        resData = response.json()
        print(f"\n用户{userid+1} {resData}")

        if 'succ' in resData:
            index += 1
            time.sleep(30)
            print(f"✅ 用户{userid+1} 阅读成功，阅读进度：{index * 0.5} 分钟")

        else:
            print(f"❌ 用户{userid+1} cookie 已过期，尝试刷新...")
            new_skey = get_wr_skey(headers, cookies)
            if new_skey:
                cookies['wr_skey'] = new_skey
                print(f"✅ 用户{userid+1} 密钥刷新成功，新密钥：{new_skey}\n🔄 重新本次阅读。")
            else:
                print(f"⚠ 用户{userid+1} 无法获取新密钥，终止运行。")
                break

        data.pop('s')

    print(f"🎉 用户{userid+1} 阅读脚本已完成！")
