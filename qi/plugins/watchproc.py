# !/usr/bin/env python
# -*- coding:utf-8 -*-

import psutil
import time
from qi.plugins.utils import *


# 操作系统监控
def start():
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
                        cl = cl + i + " "
                    pp = pp + ";pid:" + pid + "->" + cl
        write_redis("proc->" + str(pp))
        # 暂停
        time.sleep(10)


if __name__ == '__main__':
    start()
