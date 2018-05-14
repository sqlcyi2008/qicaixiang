# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re

msg = "help set\n".encode('utf-8')

file = open("d:/login.txt")
file2 = open("d:/login2.txt","w")

length = []

while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        line = re.sub(r'{[^{}]*}', '', line) #去除大括号
        line = re.sub(r'"(.*)"', '', line) #去除双引号
        line = re.sub(r'\d+,\d+?', '', line) #去除数字中的逗号
        line = re.sub(r', id=', '# id=', line) #去除返回对象中的逗号

        pattern = re.compile('"(.*)"')

        p = re.compile(r'\d+,\d+?')

        ss = line.split(',')
        ll = len(ss)

        length.append(ll)
        #print(len(ss))
        if ll == 2:
            print(line)
        #file2.write(line)

        if ll ==3:
            file2.write(str(ss[1]).strip()+"\n")

        if ll ==4:
            file2.write(str(ss[2]).strip()+"\n")


print(sorted(length))

file.close()
file2.close()

