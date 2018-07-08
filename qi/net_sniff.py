# !/usr/bin/env python
# -*- coding:utf-8 -*-

from scapy.all import *
from qi.utils import *

count = 0


def pack_callback(packet):
    p2 = packet.show(dump=True)
    # ss = str(p2).split('\n')
    # ss = str(p2).find('sport     =')
    # se = str(p2).find('\n',ss)

    '''
    p2 = str(p2).replace(' ', '')
    s2 = str(p2).splitlines()
    for line in s2:
        if line.startswith('sport'):
            print('sport=' + line)
        if line.startswith('dport'):
            print('dport=' + line)
    '''
    sport = str(packet[TCP].sport)
    dport = str(packet[TCP].dport)
    print('sport######' + sport)
    print('dport######' + dport)

    pdict = {'80': '80', '3306': '3306', 'http': 'http'}
    t = time.time()

    if sport in pdict:
        push_redis("QI_NET_SEND_" + str(sport), str(int(round(t * 1000))) + "##" + p2)

    if dport in pdict:
        push_redis("QI_NET_RECV_" + str(dport), str(int(round(t * 1000))) + "##" + p2)

    # push_redis("QI_NET_RECV_" + str(sport), str(int(round(t * 1000))) + "##" + tcp)
    # push_redis("QI_NET_RECV_" + str(sport), str(int(round(t * 1000))) + "##" + tcp)
    global count
    count = count + 1
    # push_redis('QI_NET_PACKET', count)


print(ifaces)
os.system('netstat -aon|findstr "LISTENING"')
sniff(filter="tcp port 80 or tcp port 9090", prn=pack_callback, iface="Intel(R) Dual Band Wireless-AC 8260", count=0)
# sniff(filter="tcp any", prn=pack_callback, iface="Intel(R) Ethernet Connection I219-V",count=0)
# sniff(iface="Intel(R) Ethernet Connection I219-V", prn=lambda x: x.show())
# 11     Npcap Loopback Adapter                    127.0.0.1     00:00:00:00:00:00
# 3      Sangfor SSL VPN CS Support System VNIC                  00:FF:0F:D9:74:30
# 4      Intel(R) Dual Band Wireless-AC 8260       10.72.91.190  F0:D5:BF:4A:5E:93
# 5      Bluetooth Device (Personal Area Network)                F0:D5:BF:4A:5E:97
# 9      Intel(R) Ethernet Connection I219-V       10.9.11.107   C8:5B:76:93:52:A5
