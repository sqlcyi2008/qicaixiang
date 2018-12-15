# !/usr/bin/env python
# -*- coding:utf-8 -*-
import psutil
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)

def write_redis(line):
    global r
    r.lpush("qicaixiang", line)

# 操作系统监控
def start():
    while True:
        pp = ''
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
            except psutil.NoSuchProcess:
                pass
            else:
                cl = ''
                ll = pinfo['cmdline']
                pid = str(pinfo['pid'])
                if not ll is None:
                    for i in ll:
                        cl = cl +i+" "
                    pp=pp +";pid:"+pid+"->"+cl
        write_redis("proc->"+str(pp))
        #暂停
        time.sleep(10)


if __name__ == '__main__':
    start()