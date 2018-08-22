# !/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os
import json
from qi.constants import *
from qi.utils import *
import subprocess


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/web/default.html')


class TheQRCodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('theqrcode.png')

# jdb执行命令
class JdbCmdHandler(tornado.web.RequestHandler):
    def get(self, cmd):
        if cmd == 'jdb':
            subprocess.Popen('python jdb2_start.py')
        else:
            list_lpush('QI_JDB',str(cmd))
        self.write("{'status':'ok'}")

# 远程启动进程
class ProcessHandler(tornado.web.RequestHandler):
    def get(self, name, action):
        if (name == "code"):
            print(name)
        elif (name == "pack"):
            print(name)
        elif (name == "file"):
            print(name)
        elif (name == "all"):
            print(name)
            os.popen("python openredis.py")
            os.popen("python watchproc.py")
            os.popen("python jdb_start.py")
            os.popen("python watchnet.py")
        else:
            print(name)

        self.write("{'status':'ok'}")


# 返回网络包信息
class RefreshHandler(tornado.web.RequestHandler):
    def get(self):
        ll = []
        global r
        count = r.llen("QI_NET_SEND_80")
        for key in r.keys(pattern='QI_*'):
            key = str(key, encoding="utf-8")
            # print(key + "#" + str(r.llen(key)))
            if key.startswith('QI_PROC'):
                ll.append(key + "#" + str(r.lindex('QI_PROC_127.0.0.1', 0), encoding="utf-8"))
            else:
                ll.append(key + "#" + str(r.llen(key)))
        # print(r.keys(pattern='QI_*'))
        # ltrim QI_NET_SEND_80 1 0
        '''
        for i in range(1000):
            line = r.rpop(QI_QICAIXIANG)
            if line:
                line = str(line.decode(encoding="utf-8", errors="ignore"))
                ll.append(line)
        print("###" + str(ll))
        '''
        self.write(json.dumps(ll))


# 配置调试
class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/web/debug.html')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/theqrcode.png', TheQRCodeHandler),
            (r"/process/(\w*)/(\w*)", ProcessHandler),
            (r'/debug', DebugHandler),
            (r'/jdbcmd/([\s\S]*)', JdbCmdHandler),
            (r'/refresh', RefreshHandler)
        ]

        settings = {'template_path': '.', 'static_path': 'web', 'static_url_prefix': '/web/'}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    print("访问地址:http://" + getip() + ":7788/")
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(7788)
    tornado.ioloop.IOLoop.instance().start()
