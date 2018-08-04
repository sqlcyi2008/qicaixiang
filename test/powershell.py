# -*- coding: utf-8 -*-
import subprocess


def python_call_powershell(ip):
    try:
        args = [r"powershell", r"D:\jzhou\test_ping.ps1",
                ip]  # args参数里的ip是对应调用powershell里的动态参数args[0],类似python中的sys.argv[1]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        dt = p.stdout.read()
        return dt

    return False


if __name__ == "__main__":
    ip = ["127.0.0.1"]
    print
    python_call_powershell(ip)