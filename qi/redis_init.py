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

path = os.path.abspath('.').replace('\\', '/')+'/tools'
rediszip = path + '/redis-latest.zip'
redispath = path + '/redis/'
if os.path.exists(redispath):
    # 停止服务
    os.system(redispath + 'redis-server.exe  --service-stop')
    os.system(redispath + 'redis-server.exe  --service-uninstall')
    shutil.rmtree(redispath)
    os.remove(rediszip)

url = 'https://github.com/ServiceStack/redis-windows/raw/master/downloads/redis-latest.zip'
urllib.request.urlretrieve(url, path + '/redis-latest.zip', callback)
azip = zipfile.ZipFile(rediszip)
azip.extractall(redispath)

# 在与redis-server.exe的目录中创建server_log.txt文件，否则启动失败
logdir = path + '/redis/Logs/'
logfile = logdir + 'redis_log.txt'
if not os.path.exists(logfile):
    os.mkdir(logdir)
    fp = open(logfile, 'w')
    fp.close()

# --service-uninstall
ss = path + '/redis/redis-server.exe  --service-install  ' + path + '/redis/redis.windows-service.conf --port 6379'
os.system(ss)

os.system(path + '/redis/redis-server.exe  --service-start')

# 在与redis-server.exe的目录中创建server_log.txt文件，否则启动失败
# redis-server --service-install redis.windows-service.conf --port 6379
# redis-server --service-uninstall
# redis-server --service-start
# redis-server --service-stop
