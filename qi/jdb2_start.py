# !/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import time
import random
import threading
import operator as op
from qi.utils import *
from qi.constants import *


def msgInput(msg):
    msg = (msg + '\r\n').encode('utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()


# 标准输出线程
def stdoutThread(var):
    while True:
        global proc
        line = proc.stdout.readline()
        print(line.decode('gbk'), end='')
        list_lpush('QI-JDB-OUT', line.decode('gbk'))


# 标准输入线程
def stdinThread(var):
    while True:
        # first = list_index('QI-JDB-OUT',1)
        # print(first.decode())
        el = list_brpop('QI-JDB')
        time.sleep(1)
        msgInput(el[1].decode())


def main():
    inthr = threading.Thread(target=stdinThread, args=(u'输入线程',))
    outthr = threading.Thread(target=stdoutThread, args=(u'输出线程',))

    command = '"C:\\Program Files\\Java\\jdk1.8.0_121\\bin\\jdb.exe" -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'
    global proc
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    outthr.setDaemon(True)
    outthr.start()
    inthr.setDaemon(True)
    inthr.start()

    outthr.join()
    inthr.join()


if __name__ == '__main__':
    main()
