# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time

def main():
    time.sleep(3)
    breakpoints = os.popen('findstr /n /s /d:D:/dev/SSH/SpringMVC/src "??" *.java').read()
    lines = str(breakpoints).splitlines()
    for line in lines:
        if line.find('??') > 0:
            tt=line.split(':')
            print(str(tt[0]).replace('\\','.').replace('.java','')+':'+str(tt[1]))


    #print(lines)

if __name__ == '__main__':
    while True:
        main()
