# !/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess
import time
import threading

def stdinThread(var):
    time.sleep(3)
    print("in....start")


    msg = "n\n".encode('utf-8')
    global proc
    proc.stdin.write(msg)
    proc.stdin.flush()
    time.sleep(3)

    msg = "list\n".encode('utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()
    time.sleep(3)


    msg = "cont\n".encode('utf-8')

    proc.stdin.write(msg)
    proc.stdin.flush()

    print("in....end")


def stdoutThread(var):
    print("out....start")
    while True:
        global proc
        line = proc.stdout.readline()
        #需要判空缓冲区
        if line:
            print(line)

    print("out....end")

global proc
if __name__ == '__main__':
    inthr = threading.Thread(target=stdinThread, args=(u'输入线程',))
    outthr = threading.Thread(target=stdoutThread, args=(u'输出线程',))

    #command="redis-cli"
    #command = '"C:\\Program Files\\Java\\jdk1.8.0_121\\bin\\jdb.exe" -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'
    command="python D:\\dev\\PycharmProjects\\qicaixiang\\test\\pdbtest.py"
    global proc
    proc = subprocess.Popen(command,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    inthr.setDaemon(True)
    inthr.start()

    outthr.setDaemon(True)
    outthr.start()

    outthr.join()
    inthr.join()
