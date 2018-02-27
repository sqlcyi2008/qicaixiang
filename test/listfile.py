# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import subprocess

def IterateFiles_CMD(directory):
    assert os.path.isdir(directory),'make sure directory argument should be a directory'
    cmd = 'dir /s /B /A-D ' + directory
    ret = []
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    for line in p.stdout.readlines():
        ret.append(line)

    if p.wait() == 0:
        return ret