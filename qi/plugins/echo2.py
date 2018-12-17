#!/usr/bin/python
from sys import stdout
from time import sleep
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)

# Count from 1 to 10 with a sleep
# for count in range(0, 10):
#   print(r.brpop('qiwebstdout'))
#   stdout.flush()
#   sleep(1)

for count in range(0, 1000):
  r.lpush('qiwebstdout',str(count))
  sleep(0.1)


#LPUSH qiwebstdout mongodb1
#LPUSH qiwebstdout mongodb2
#LPUSH qiwebstdout mongodb3
#LPUSH qiwebstdout mongodb4
#LPUSH qiwebstdout mongodb5
#LPUSH qiwebstdout mongodb6
#LPUSH qiwebstdout mongodb7
#LPUSH qiwebstdout mongodb8

