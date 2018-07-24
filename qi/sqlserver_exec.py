# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os

def main():
    print(os.popen('sqlcmd -S LICHUANYI02\SQLEXPRESS -d demo -U sa -P 123456a? -Q "sp_help student"').read())
    print(os.popen('sqlcmd -S LICHUANYI02\SQLEXPRESS -d demo -U sa -P 123456a? -Q "select name from sysobjects where xtype=\"u\""').read())


if __name__ == '__main__':
    main()
