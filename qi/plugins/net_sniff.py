# !/usr/bin/env python
# -*- coding:utf-8 -*-

from scapy.all import *
from qi.plugins.utils import *


def pack_callback(packet):
    p2 = packet.show(dump=True)
    print(p2)

    '''
    存在IPv6的问题
     type      = IPv6
     ###[ IPv6 ]### 
     version   = 6
    '''
    src = str(packet[IPv6].src)
    dst = str(packet[IPv6].dst)
    sport = str(packet[TCP].sport)
    dport = str(packet[TCP].dport)

    pdict = {'3306': '3306', '9090': '9090'}
    t = time.time()

    if sport in pdict:
        push_redis('QI_NET_SEND_' + src + '_' + str(sport), str(int(round(t * 1000))) + "##" + p2)

    if dport in pdict:
        push_redis("QI_NET_RECV_" + dst + '_' + str(dport), str(int(round(t * 1000))) + "##" + p2)


print(ifaces)
os.system('netstat -aon|findstr "LISTENING"')

#filter要与上面的端口字典保持一致
sniff(filter="tcp port 3306 or tcp port 9090", prn=pack_callback, iface="Npcap Loopback Adapter", count=0)
# sniff(filter="tcp any", prn=pack_callback, iface="Intel(R) Ethernet Connection I219-V",count=0)
# sniff(iface="Intel(R) Ethernet Connection I219-V", prn=lambda x: x.show())
# 11     Npcap Loopback Adapter                    127.0.0.1     00:00:00:00:00:00
# 3      Sangfor SSL VPN CS Support System VNIC                  00:FF:0F:D9:74:30
# 4      Intel(R) Dual Band Wireless-AC 8260       10.72.91.190  F0:D5:BF:4A:5E:93
# 5      Bluetooth Device (Personal Area Network)                F0:D5:BF:4A:5E:97
# 9      Intel(R) Ethernet Connection I219-V       10.9.11.107   C8:5B:76:93:52:A5
