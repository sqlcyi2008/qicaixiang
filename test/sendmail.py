# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
os.system('cmd /c blat -install smtp.163.com lcyi_176@163.com')
# os.system('cmd /c blat d:\mail.txt -to lcyi_176@163.com -attach "D:\lichuanyi\备案-李传义.jpg" -s "备案-李传义.jpg" -u lcyi_176@163.com -pw lcyi176 -charset gb2312')
#print(os.popen('cmd /c blat d:\mail.txt -to lcyi_176@163.com -attach "D:\lichuanyi\备案-李传义.jpg" -s "备案-李传义.jpg" -u lcyi_176@163.com -pw lcyi176 -charset gb2312').read())
flag = True
path = 'D:\\lichuanyi\\A李家林\\'
for fpathe, dirs, fs in os.walk(path):
    for f in fs:
        file = os.path.splitext(f)
        filename, type = file
        #print(filename)
        #print(type)
        print(os.path.join(fpathe, f))
        if type == '.jpeg' or type == '.jpg' or type == '.JPG':
            print('####'+filename[0])
            if filename[0]!='.':
                print('!!!!')
                print(os.popen(
                    'cmd /c blat d:\mail.txt -to lcyi_176@163.com -attach '
                    +os.path.join(fpathe, f)+' -s '+'A李家林#图片#'+os.path.join(fpathe, f)+' '
                    '-u lcyi_176@163.com -pw lcyi176 -charset gb2312').read())
                time.sleep(5)
            # exit()