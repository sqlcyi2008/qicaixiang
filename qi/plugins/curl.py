# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from const import const
import urllib.request
import zipfile
import subprocess
import threading
from qi.plugins.utils import *

const.CURLURL = "https://curl.haxx.se/windows/dl-7.63.0/curl-7.63.0-win64-mingw.zip"
const.CURLNAME = "curl-7.63.0-win64-mingw.zip"
const.CURLPATH = const.CURLNAME.replace(".zip", "")
const.CURLEXE = "curl.exe"

# 标准输出线程
def stdoutThread(var):
    while True:
        global proc
        line = proc.stdout.readline()
        if not line:
            break  # 关闭子进程时，会一直输出空行，故跳出
        print(line.decode(), end='')
        list_lpush('qiwebstdout', line.decode())
        #list_lpush('runoobkey', "status ok!")

def main():
    #inthr = threading.Thread(target=stdinThread, args=(u'输入线程',))
    outthr = threading.Thread(target=stdoutThread, args=(u'输出线程',))

    el = list_brpop('curl-key')
    curlargs=el[1].decode()
    command =const.VENDORPATH + const.CURLPATH + "/bin/" + const.CURLEXE + "  "+curlargs
    global proc
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    outthr.setDaemon(True)
    outthr.start()
    outthr.join()

def callback(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    # 输出报错
    # print('%.2f%%' % per)


def init():
    urllib.request.urlretrieve(const.CURLURL, const.VENDORPATH + const.CURLNAME, callback)
    azip = zipfile.ZipFile(const.VENDORPATH + const.CURLNAME)
    azip.extractall(const.VENDORPATH)


if __name__ == '__main__':

    if len(sys.argv) >= 2:
        fn = sys.argv[1]
        eval(fn)()
    else:
        main()
