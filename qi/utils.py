# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import socket
from qi.constants import *

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)

def write_redis(line):
    global r
    r.lpush(QI_QICAIXIANG, line)


def read_redis():

    while True:
        global r
        line = r.rpop(QI_QICAIXIANG)
        if line:
            print(">>>" + str(line.decode(encoding="utf-8", errors="ignore")))

def rpop_redis():
    global r
    line = r.rpop(QI_QICAIXIANG)
    return line


def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip