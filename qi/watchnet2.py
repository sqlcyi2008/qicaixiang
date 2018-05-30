# !/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import dpkt
import time
from qi.utils import *
from qi.constants import *

# 抓包进程执行代码:
def main():
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    myip = getip()
    print("@"+myip)
    sniffer.bind((myip, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ipp = dpkt.ip.IP(raw_buffer)
            tt = ipp.data.__class__.__name__;
            if tt == 'TCP' or tt == 'UDP':
                pp = ipp.data.dport;
                if pp != 80:
                    continue

                tcp = ''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                    t = time.time()
                    print(str(int(round(t * 1000))) + "##" + tt + ":" + str(len(str(ipp.data)))+"@"+tcp)
                except Exception as e:
                    print(e)
                if tcp.startswith('GET') or tcp.startswith('POST'):
                    line = tcp.splitlines()[0]
                    print(line)
                    #write_redis("http->" + line)
    except KeyboardInterrupt:
        pass
    # disabled promiscuous mode
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
