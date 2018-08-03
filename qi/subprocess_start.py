# !/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import time
import random
import threading
import operator as op
from qi.utils import *
from qi.constants import *

"""
jdb命令
trace [go] method exit | exits
"""


def msgInput(msg):
    msg = (msg + '\r\n').encode('utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()

global cmd
cmd = ''

# 标准输出线程
def stdoutThread(var):
    while True:
        global proc
        line = proc.stdout.readline()
        qq = str(line.decode()).replace('\r\n','')
        #print('#####'+qq, end='')
        print('#####'+qq)
        if op.eq(qq,'7'):
            global cmd
            cmd = 'winner winner, chicken dinner.'

# 标准输入线程
def stdinThread(var):
    while True:
        #el = brpop_redis('QI-JDB')
        #print(el[1].decode())

        time.sleep(0.5)
        global cmd
        if op.eq(cmd,''):
            msgInput(str(random.randint(0, 9)))
        else:
            msgInput(cmd)
            cmd = ''


def main():
    inthr = threading.Thread(target=stdinThread, args=(u'输入线程',))
    outthr = threading.Thread(target=stdoutThread, args=(u'输出线程',))

    command = 'd:/inout.bat'
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
