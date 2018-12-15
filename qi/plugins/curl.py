# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from const import const
import urllib.request
import zipfile

const.CURLURL = "https://curl.haxx.se/windows/dl-7.63.0/curl-7.63.0-win64-mingw.zip"
const.CURLNAME = "curl-7.63.0-win64-mingw.zip"
const.CURLPATH = const.CURLNAME.replace(".zip", "")
const.CURLEXE = "curl.exe"


def main():
    # os.popen(const.VENDORPATH + const.CURLPATH + "/bin/" + const.CURLEXE).read()
    os.system(const.VENDORPATH + const.CURLPATH + "/bin/" + const.CURLEXE)


def callback(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    #输出报错
    #print('%.2f%%' % per)


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
