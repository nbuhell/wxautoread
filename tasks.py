import random
import threading
import time
from users import users
from read import read
from randomdata import data as rddata


def task(idx):
    user = users[idx]
    data = random.choice(rddata[idx])
    read(user['headers'], user['cookies'], data, idx)


# 创建线程
thread1 = threading.Thread(target=task, args=(0,))  # 任务 A 执行 2 秒
thread2 = threading.Thread(target=task, args=(1,))  # 任务 B 执行 4 秒

# 启动线程
thread1.start()
time.sleep(30)
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("所有任务完成")
