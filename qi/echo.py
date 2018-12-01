#!/usr/bin/python
from sys import stdout
from time import sleep
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)

# Count from 1 to 10 with a sleep
# for count in range(0, 10):
#   print(r.brpop('runoobkey'))
#   stdout.flush()
#   sleep(1)

while True:
  print(r.brpop('runoobkey'))
  stdout.flush()


#LPUSH runoobkey mongodb1
#LPUSH runoobkey mongodb2
#LPUSH runoobkey mongodb3
#LPUSH runoobkey mongodb4
#LPUSH runoobkey mongodb5
#LPUSH runoobkey mongodb6
#LPUSH runoobkey mongodb7
#LPUSH runoobkey mongodb8

