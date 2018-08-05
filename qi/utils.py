# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import socket
from qi.constants import *

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)


def push_redis(key, line):
    global r
    r.lpush(key, line)


def list_lpush(key, line):
    global r
    r.lpush(key, line)


def list_brpop(key):
    global r
    # 返回值为元组
    el = r.brpop(key)
    return el


def list_index(key,i):
    global r
    # 返回值为元组
    el = r.lindex(key,i)
    return el


def write_redis(line):
    global r
    r.lpush(QI_QICAIXIANG, line)


def read_redis():
    while True:
        global r
        # line = r.rpop(QI_QICAIXIANG)
        line = r.brpop(QI_QICAIXIANG)  # 阻塞模式
        if line:
            print(str(line[1].decode(encoding="utf-8", errors="ignore")))


def write_event_redis(event):
    global r
    r.lpush(QI_EVENT_QUEUE, event)


def read_event_redis():
    while True:
        global r
        line = r.brpop(QI_QICAIXIANG)  # 阻塞模式
        if line:
            print(str(line[1].decode(encoding="utf-8", errors="ignore")))


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
