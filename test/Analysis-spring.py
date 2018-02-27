# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re

file = open("d:/springmvc6.txt")
file2 = open("d:/springmvc5.txt","w")

length = []

lines = file.readlines(100000)
lastY = 0
thisY = 0
thisX = 0
for line in lines:
    if "已进入方法" in str(line):
        thisY = lastY + 1
    elif "已退出方法" in str(line):
        thisY = lastY - 1
    else:
        continue

    lastY = thisY
    thisX=thisX+1
    print(str(thisX))
    print(str(thisY))

    line = re.sub(r'{[^{}]*}', '', line) #去除大括号
    line = re.sub(r'"(.*)"', '', line) #去除双引号
    line = re.sub(r'\d+,\d+?', '', line) #去除数字中的逗号
    line = re.sub(r', id=', '# id=', line) #去除返回对象中的逗号

    ss = line.split(',')
    ll = len(ss)
    length.append(ll)
    #print(len(ss))
    if ll == 2:
        pass
    #file2.write(line)

    if ll ==3:
        file2.write(str(ss[1]).strip()+"\n")

    if ll ==4:
        file2.write(str(ss[2]).strip()+"\n")

#print(sorted(length))

file.close()
file2.close()

