
import json
import os

headers = [{
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=dev-1744355656859,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=434bb0c01fc041eca00fd9b8f7873f8e',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://weread.qq.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://weread.qq.com/web/reader/ce032b305a9bc1ce0b0dd2ak98d321b025d98dce83da05a',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '434bb0c01fc041eca00fd9b8f7873f8e-b4ac382e06a93d30',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
},
    {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=dev-1744355656859,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=bde79dcdff064c39bcb49bca1216575b',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://weread.qq.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://weread.qq.com/web/reader/db8329d071cc7f70db8a479k45c322601945c48cce2e120',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'bde79dcdff064c39bcb49bca1216575b-94a0c1223e54c037',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
}
]

def readfile():
    with open('cookies.txt', 'r') as f:
         content = f.read()
    return content

env_cookies = os.getenv('WXREAD_COOKIES')
if not env_cookies:
    env_cookies = readfile()
cookies = json.loads(json.dumps(eval(env_cookies))) if env_cookies else []
