#! /usr/bin/env python
#-*- coding:utf-8 -*-

import time
import random
from influxdb import InfluxDBClient


def read_info():
    cpu_time_info = [1,2,3,5,6]

    cpu_time_info[0] = random.randint(0, 99)
    cpu_time_info[1] = random.randint(0, 99)
    cpu_time_info[2] = random.randint(0, 99)
    cpu_time_info[3] = random.randint(0, 99)
    cpu_time_info[4] = random.randint(0, 99)

    data_list = [{'measurement': 'win',
                 'tags': {'cpu': 'i7-7700HQ'},
                 'fields': {'cpu_info_user': cpu_time_info[0],
                            'cpu_info_system': cpu_time_info[1],
                            'cpu_info_idle': cpu_time_info[2],
                            'cpu_info_interrupt': cpu_time_info[3],
                            'cpu_info_dpc': cpu_time_info[4]}}]
    return data_list

if __name__ == '__main__':
    #client = InfluxDBClient(host, port, user, password, database)  # 初始化
    client = InfluxDBClient('localhost', 8086, 'root', '', 'mydb')  # 初始化
    counts = 0  #计数,也就是数据上传20次
    while counts <= 2000:#
        counts += 1
        client.write_points(read_info())
        #time.sleep(5)