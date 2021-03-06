# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import socket
import dpkt

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)


def write_redis(line):
    global r
    r.lpush("qicaixiang", line)


def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# 抓包进程执行代码:
def main():
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    myip = getip()
    sniffer.bind((myip, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ipp = dpkt.ip.IP(raw_buffer)
            print("##"+str(ipp.data))
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 8080:
                tcp = ''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                if tcp.startswith('GET') or tcp.startswith('POST'):
                    line = tcp.splitlines()[0]
                    write_redis("http->" + line)

            # mysql
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 3306:
                tcp = ''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                write_redis("sql2->" + tcp)

            # oracle
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 1521:
                # print (ipp.data.data)   ignore
                tcp = ''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                write_redis("sql2->" + tcp)

            # sqlserver
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 1433:
                tcp = ''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                write_redis("sql2->" + tcp)

    except KeyboardInterrupt:
        pass
    # disabled promiscuous mode
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
