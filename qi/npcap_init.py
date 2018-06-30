# !/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib.request
import os


def callback(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


path = os.path.abspath('.').replace('\\', '/')
npcap = path + '/npcap-0.99-r6.exe'

if os.path.exists(npcap):
    os.remove(npcap)

# exit()

url = 'https://nmap.org/npcap/dist/npcap-0.99-r6.exe'
urllib.request.urlretrieve(url, path + '/npcap-0.99-r6.exe', callback)

os.system(path + '/npcap-0.99-r6.exe')
