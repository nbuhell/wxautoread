import random
from users import headers, cookies
from read import read
from randomdata import data as rddata


header = headers[0]
cookie = cookies[0]
data = random.choice(rddata[0])
print(data["sm"])
read(header, cookie, data, 0)
