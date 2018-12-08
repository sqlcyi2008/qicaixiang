# -*- coding:utf-8 -*-

import urllib.request
import os
import zipfile
import shutil

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

path = os.path.abspath('.').replace('\\', '/')+'/vendor'
rediszip = path + '/websocketd-0.3.0-windows_amd64.zip'
redispath = path + '/websocketd/'
if os.path.exists(redispath):
    shutil.rmtree(redispath)
    os.remove(rediszip)

#exit()

url = 'https://github.com/joewalnes/websocketd/releases/download/v0.3.0/websocketd-0.3.0-windows_amd64.zip'
urllib.request.urlretrieve(url, path + '/websocketd-0.3.0-windows_amd64.zip', callback)
azip = zipfile.ZipFile(rediszip)
azip.extractall(redispath)