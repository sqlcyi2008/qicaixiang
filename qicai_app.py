# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import socket
import dpkt
from multiprocessing import Process, Queue
import json
import psutil
import subprocess
import time
import threading
import os
import constants

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)

def write_redis(line):
    global r
    r.lpush("qicaixiang", line)

def read_redis():
    global r
    #str = r.rpop('qicaixiang')
    while True:
        #list =  r.lrange("qicaixiang",0,100)
        line = r.rpop('qicaixiang')
        if line:
            print(">>>"+str(line.decode(encoding="utf-8", errors="ignore")))

        #time.sleep(3)

def start_redis():
    os.system('D:/program/Redis-x64-3.2.100/redis-server.exe D:/program/Redis-x64-3.2.100/redis.windows.conf')


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/static/docs/home.html')

class TheQRCodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('theqrcode.png')

#远程启动进程
class ProcessHandler(tornado.web.RequestHandler):
    def get(self,name,action):
        if(name=="code"):
            global jdb
            if(action=="start"):
                jdb = Process(target=exec_jdb, args=())
                jdb.start()
            else:
                jdb.terminate()
        elif(name=="pack"):
            pw = Process(target=capture_packet, args=())
            pw.start()
        elif(name=="file"):
            fw = Process(target=file_watch, args=())
            fw.start()
        elif(name == "all"):
            jdb = Process(target=exec_jdb, args=())
            jdb.start()
            pw = Process(target=capture_packet, args=())
            pw.start()
            fw = Process(target=file_watch, args=())
            fw.start()
        else:
            print(name)

        self.write("{'status':'ok'}")

# 返回网络包信息
class RefreshHandler(tornado.web.RequestHandler):
    def get(self):
        ll = []
        global r
        for i in range(100):
            line = r.rpop('qicaixiang')
            if line:
                line = str(line.decode(encoding="utf-8", errors="ignore"))
                ll.append(line)
        print("###" + str(ll))
        self.write(json.dumps(ll))

#配置调试
class DebuggerHandler(tornado.web.RequestHandler):
    def post(self):
        cmd = self.get_arguments("cmd")
        global r
        r.set(constants.QI_JAVA_CMDLINE,cmd[0])
        #self.write(cmd[0])

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/theqrcode.png', TheQRCodeHandler),
            (r"/process/(\w*)/(\w*)", ProcessHandler),
            (r'/debugger', DebuggerHandler),
            (r'/refresh', RefreshHandler)
        ]

        settings = {'template_path': '.','static_path':'static','static_url_prefix':'/static/'}
        tornado.web.Application.__init__(self, handlers, **settings)

# 操作系统监控
def os_watch():
    while True:
        pp = ''
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
            except psutil.NoSuchProcess:
                pass
            else:
                cl = ''
                ll = pinfo['cmdline']
                pid = str(pinfo['pid'])
                if not ll is None:
                    for i in ll:
                        cl = cl +i+" "
                    pp=pp +";pid:"+pid+"->"+cl
        write_redis("proc->"+str(pp))
        #暂停
        time.sleep(10)

# 抓包进程执行代码:
def capture_packet():
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    myip = get_ip()
    sniffer.bind((myip, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ipp = dpkt.ip.IP(raw_buffer)
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 7788:
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                if tcp.startswith('GET') or tcp.startswith('POST'):
                    line = tcp.splitlines()[0]
                    write_redis("http->" + line)

            #mysql
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 3306:
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                write_redis("sql2->" + tcp)

            #oracle
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 1521:
                #print (ipp.data.data)   ignore
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                write_redis("sql2->"+tcp)

            #sqlserver
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 1433:
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                write_redis("sql2->"+tcp)

    except KeyboardInterrupt:
        pass
    # disabled promiscuous mode
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

#获取本机默认IP地址
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def exec_jdb():
    os.system('python.exe exec_jdb.py')


def file_watch():
    os.system('python.exe file_watch.py')


def start_server():
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(7788)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    sr = Process(target=start_redis, args=())
    sr.start()

    #jdb = Process(target=exec_jdb, args=())
    #jdb.start()

    #pw = Process(target=capture_packet, args=())
    #pw.start()

    ow = Process(target=os_watch, args=())
    ow.start()

    #fw = Process(target=file_watch, args=())
    #fw.start()

    ss = Process(target=start_server, args=())
    ss.start()

    #read_redis()
    print("IP:"+get_ip())
    #print("@@@"+constants.QI_FILE_TYPE)