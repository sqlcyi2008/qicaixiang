# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from qi.plugins.utils import *

while True:
    tasks = os.popen('tasklist').read()
    count = str(tasks).count('\n')
    push_redis("QI_PROC_127.0.0.1", count)
    time.sleep(5)
