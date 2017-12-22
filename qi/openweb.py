# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import socket
import json
import qi.constants

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)


def write_redis(line):
    global r
    r.lpush("qicaixiang", line)


def read_redis():
    global r
    # str = r.rpop('qicaixiang')
    while True:
        # list =  r.lrange("qicaixiang",0,100)
        line = r.rpop('qicaixiang')
        if line:
            print(">>>" + str(line.decode(encoding="utf-8", errors="ignore")))


def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/static/docs/a.html')


class TheQRCodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('theqrcode.png')


# 远程启动进程
class ProcessHandler(tornado.web.RequestHandler):
    def get(self, name, action):
        if (name == "code"):
            global jdb
            if (action == "start"):
                print(name)
                # jdb = Process(target=exec_jdb, args=())
                # jdb.start()
            else:
                print(name)
                # jdb.terminate()
        elif (name == "pack"):
            print(name)
            # pw = Process(target=capture_packet, args=())
            # pw.start()
        elif (name == "file"):
            print(name)
            # fw = Process(target=file_watch, args=())
            # fw.start()
        elif (name == "all"):
            print(name)
            # jdb = Process(target=exec_jdb, args=())
            # jdb.start()
            # pw = Process(target=capture_packet, args=())
            # pw.start()
            # fw = Process(target=file_watch, args=())
            # fw.start()
        else:
            print(name)

        self.write("{'status':'ok'}")


# 返回网络包信息
class RefreshHandler(tornado.web.RequestHandler):
    def get(self):
        ll = []
        global r
        for i in range(1000):
            line = r.rpop('qicaixiang')
            if line:
                line = str(line.decode(encoding="utf-8", errors="ignore"))
                ll.append(line)
        print("###" + str(ll))
        self.write(json.dumps(ll))


# 配置调试
class DebuggerHandler(tornado.web.RequestHandler):
    def post(self):
        cmd = self.get_arguments("cmd")
        global r
        r.set(qi.constants.QI_JAVA_CMDLINE, cmd[0])

        # self.write(cmd[0])


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/theqrcode.png', TheQRCodeHandler),
            (r"/process/(\w*)/(\w*)", ProcessHandler),
            (r'/debugger', DebuggerHandler),
            (r'/refresh', RefreshHandler)
        ]

        settings = {'template_path': '.', 'static_path': '../static', 'static_url_prefix': '/static/'}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    print("本机地址:" + getip())
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(7788)
    tornado.ioloop.IOLoop.instance().start()
