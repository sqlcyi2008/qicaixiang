# -*- coding:utf-8 -*-

import urllib.request
import os
import zipfile

def callback(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print ('%.2f%%' % per)

path = os.path.abspath('.').replace('\\','/')
url = 'https://github.com/ServiceStack/redis-windows/raw/master/downloads/redis-latest.zip'
urllib.request.urlretrieve(url,path+'/redis-latest.zip' ,callback)
azip = zipfile.ZipFile(path+'/redis-latest.zip')
azip.extractall(path+'/redis')

#--service-uninstall
#ss = path+'/redis/redis-server.exe --service-install '+path+'/redis/redis.windows-service.conf --loglevel verbos'
#os.popen(ss)

