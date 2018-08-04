# !/usr/bin/env python
# -*- coding:utf-8 -*-

'''
python3 安装scapy-python3
注：linux，可能需要以root登陆，避免出现permission error
Scapy还包含内建函数arping(),该函数实现的功能和以上的两个命令类似：
arping("192.168.1.*")
'''
from scapy.all import *
conf.verb = 0

p = scapy.all.IP(dst="163.com")/scapy.all.TCP()
r = sr1(p)
print(r.summary())

#https://nmap.org/npcap/dist/npcap-0.99-r6.exe