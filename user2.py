import random
from users import headers, cookies 
from read import read
from randomdata import data as rddata


header = headers[1]
cookie = cookies[1]
data = random.choice(rddata[1])
print(data["sm"])
read(header, cookie, data, 1)
