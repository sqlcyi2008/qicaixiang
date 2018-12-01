# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def main():
    result = os.popen('D:/dev/PycharmProjects/qicaixiang/qi/vendor/redis/redis-cli.exe -h 127.0.0.1 -p 6379 set lichuanyi hello').read()
    os.popen('D:/dev/PycharmProjects/qicaixiang/qi/vendor/redis/redis-cli.exe -h 127.0.0.1 -p 6379 lpush stdout '+result).read()

if __name__ == '__main__':
    main()
