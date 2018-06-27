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
    sniffer_ip = getip()
    print("@" + sniffer_ip)
    sniffer.bind((sniffer_ip, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)
            ipp = dpkt.ip.IP(raw_buffer[0])
            tt = ipp.data.__class__.__name__;
            if tt == 'TCP':
                dport = ipp.data.dport;
                sport = ipp.data.sport;
                dict = {'80': '80', '8080': '8080', '3306': '3306', '1433': '1433'}
                print(str(sport) + ">>" + str(dport))
                if dport == 6379 or sport == 6379:
                    pass

                tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                try:
                    t = time.time()
                    # print(str(int(round(t * 1000))) + "##" + tt + ":" + str(len(str(ipp.data)))+"@"+str(dport))
                    print("QI_NET_RECV_" + str(sport) + "||" + str(int(round(t * 1000))) + "##")
                    push_redis("QI_NET_RECV_" + str(sport), str(int(round(t * 1000))) + "##" + tcp)
                except Exception as e:
                    print(e)

    except KeyboardInterrupt:
        pass
    # disabled promiscuous mode
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    main()
