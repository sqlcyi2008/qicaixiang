# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def main():
    os.system('mysql -hlocalhost -P3306 -uroot -proot imcoo -e "describe person"')
    os.system('mysql -hlocalhost -P3306 -uroot -proot imcoo -e "select * from person"')


if __name__ == '__main__':
    main()
