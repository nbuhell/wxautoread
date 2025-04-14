import os
import json
import requests
import time
import hashlib
import urllib.parse
import random

# 加密盐及其它默认值
KEY = "3c5c8717f3daf09iop3423zafeqoi"
COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
READ_URL = "https://weread.qq.com/web/book/read"
RENEW_URL = "https://weread.qq.com/web/login/renewal"
FIX_SYNCKEY_URL = "https://weread.qq.com/web/book/chapterInfos"


# github action部署用
# 从环境变量获取 headers、cookies等值(如果不存在使用默认本地值)
# 每一次代表30秒，比如你想刷1个小时这里填120，你只需要签到这里填2次

env_num = os.getenv('READ_NUM')

# headers = json.loads(json.dumps(eval(env_headers))
#                      ) if env_headers else local_headers
# cookies = json.loads(json.dumps(eval(env_cookies))
#                      ) if env_cookies else local_cookies
READ_NUM = int(env_num) if env_num not in (None, '') else 120


def encode_data(data):
    """数据编码"""
    return '&'.join(f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys()))


def cal_hash(input_string):
    """计算哈希值"""
    _7032f5 = 0x15051505
    _cc1055 = _7032f5
    length = len(input_string)
    _19094e = length - 1

    while _19094e > 0:
        _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
        _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
        _19094e -= 2

    return hex(_7032f5 + _cc1055)[2:].lower()

def get_wr_skey(headers, cookies):
    """刷新cookie密钥"""
    response = requests.post(RENEW_URL, headers=headers, cookies=cookies,
                             data=json.dumps(COOKIE_DATA, separators=(',', ':')))
    for cookie in response.headers.get('Set-Cookie', '').split(';'):
        if "wr_skey" in cookie:
            return cookie.split('=')[-1][:8]
    return None

def fix_no_synckey(headers, cookies):
    requests.post(FIX_SYNCKEY_URL, headers=headers, cookies=cookies,
                             data=json.dumps({"bookIds":["3300060341"]}, separators=(',', ':')))

def refresh_cookie(headers, cookies):
    print(f"🍪 刷新cookie")
    new_skey = get_wr_skey(headers, cookies)
    if new_skey:
        cookies['wr_skey'] = new_skey
        print(f"✅ 密钥刷新成功，新密钥：{new_skey}")
        print(f"🔄 重新本次阅读。")
    else:
        ERROR_CODE = "❌ 无法获取新密钥或者配置有误，终止运行。"
        print(ERROR_CODE)
        #push(ERROR_CODE, PUSH_METHOD)
        raise Exception(ERROR_CODE)
    
def read(headers, cookies, data, userid):
    refresh_cookie(headers, cookies)
    index = 1
    lastTime = int(time.time()) - 30
    while index <= READ_NUM:
        if 's' in data:
            data.pop('s')
        # data['b'] = random.choice(book)
        # data['c'] = random.choice(chapter)
        thisTime = int(time.time())
        data['ct'] = thisTime
        data['rt'] = thisTime - lastTime
        data['ts'] = int(thisTime * 1000) + random.randint(0, 1000)
        data['rn'] = random.randint(0, 1000)
        data['sg'] = hashlib.sha256(f"{data['ts']}{data['rn']}{KEY}".encode()).hexdigest()
        data['s'] = cal_hash(encode_data(data))

        print(f"⏱️ 尝试第 {index} 次阅读...")
        print(f"📕 data: {data}")
        response = requests.post(READ_URL, headers=headers, cookies=cookies, data=json.dumps(data, separators=(',', ':')))
        resData = response.json()
        print(f"📕 response: {resData}")

        if 'succ' in resData:
            if 'synckey' in resData:
                lastTime = thisTime
                index += 1
                time.sleep(30)
                print(f"✅ 阅读成功，阅读进度：{(index - 1) * 0.5} 分钟")
            else:
                print("❌ 无synckey, 尝试修复...")
                fix_no_synckey(headers, cookies)
        else:
            print("❌ cookie 已过期，尝试刷新...")
            refresh_cookie(cookies)

    print(f"🎉 用户{userid+1} 阅读脚本已完成！")


# def cal_hash(input_string):
#     _7032f5 = 0x15051505
#     _cc1055 = _7032f5
#     length = len(input_string)
#     _19094e = length - 1

#     while _19094e > 0:
#         _7032f5 = 0x7fffffff & (_7032f5 ^ ord(
#             input_string[_19094e]) << (length - _19094e) % 30)
#         _cc1055 = 0x7fffffff & (_cc1055 ^ ord(
#             input_string[_19094e - 1]) << _19094e % 30)
#         _19094e -= 2

#     return hex(_7032f5 + _cc1055)[2:].lower()


# def get_wr_skey(headers, cookies):
#     response = requests.post(RENEW_URL, headers=headers, cookies=cookies,
#                              data=json.dumps(COOKIE_DATA, separators=(',', ':')))
#     for cookie in response.headers.get('Set-Cookie', '').split(';'):
#         if "wr_skey" in cookie:
#             return cookie.split('=')[-1][:8]
#     return None


# def read(headers, cookies, data, userid):
#     index = 1
#     headers['referer'] = referer_url + data['b']
#     while index <= number:
#         data['ct'] = int(time.time())
#         data['ts'] = int(time.time() * 1000)
#         data['rn'] = random.randint(0, 1000)
#         data['sg'] = hashlib.sha256(
#             f"{data['ts']}{data['rn']}{KEY}".encode()).hexdigest()
#         data['s'] = cal_hash(encode_data(data))
#         print(f"\n用户{userid+1} 尝试第 {index} 次阅读...")
#         response = requests.post(READ_URL, headers=headers, cookies=cookies, data=json.dumps(
#             data, separators=(',', ':')))
#         resData = response.json()
#         print(f"\n用户{userid+1} {resData}")

#         if 'succ' in resData:
#             index += 1
#             time.sleep(30)
#             print(f"✅ 用户{userid+1} 阅读成功，阅读进度：{index * 0.5} 分钟")

#         else:
#             print(f"❌ 用户{userid+1} cookie 已过期，尝试刷新...")
#             new_skey = get_wr_skey(headers, cookies)
#             if new_skey:
#                 cookies['wr_skey'] = new_skey
#                 print(f"✅ 用户{userid+1} 密钥刷新成功，新密钥：{new_skey}\n🔄 重新本次阅读。")
#             else:
#                 print(f"⚠ 用户{userid+1} 无法获取新密钥，终止运行。")
#                 break

#         data.pop('s')

#     print(f"🎉 用户{userid+1} 阅读脚本已完成！")
