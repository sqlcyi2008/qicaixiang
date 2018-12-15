import subprocess
import time
import threading
from time import ctime, sleep
import redis
import constants

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
global r
r = redis.Redis(connection_pool=pool)


def write_redis(line):
    # print("jdb write redis.")
    global r
    r.lpush("qicaixiang", line)


# 标准输出线程
def stdoutThread(var):
    while True:
        global proc
        line = proc.stdout.readline()
        if not line:
            break
        line = line.decode('gbk')
        # print(line)
        write_redis("code->" + line)
        if 'Server startup in' in line:
            msg = 'trace go method exits\r\n'.encode('utf-8')
            #msg = 'trace go methods\r\n'.encode('utf-8')
            # trace [go] method exit | exits
            #msg = 'stop at com.inspur.sw.stpptnr.cmd.StPptnRCommand:706\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()

        if '断点命中:' in line:
            print("duandian="+line)
            msg = 'locals\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()

            msg = 'cont\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()


# 标准输入线程
def stdinThread(var):
    # 等待服务器启动完成
    time.sleep(10)
    cmd = []
    cmd.insert(0, 'stop at com.inspur.sw.stpptnr.cmd.StPptnRCommand:706\r\n')
    cmd.insert(0, 'locals\r\n')
    cmd.insert(0, 'cont\r\n')
    while False:
        line = cmd.pop()
        if line:
            global proc
            msg = line.encode('utf-8')
            print("jdb==" + line)
            # proc.stdin.write(msg)
            # proc.stdin.flush()
            time.sleep(1)


def formatCmd(line):
    line = line[line.find('->') + 2:].replace('\\', '/')
    java = "\"" + line[:line.find('java.exe') + 8].replace('java.exe', 'jdb.exe') + "\""
    options = line[line.find('java.exe') + 8:]
    return java + " -launch " + options


def main():
    inthr = threading.Thread(target=stdinThread, args=(u'输入线程',))
    outthr = threading.Thread(target=stdoutThread, args=(u'输出线程',))

    global r
    line = r.get(constants.QI_JAVA_CMDLINE)

    #command = formatCmd(line.decode(encoding="utf-8", errors="ignore"))

    # command = 'jdb.exe -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'
    command = '"C:\\Program Files\\Java\\jdk1.8.0_121\\bin\\jdb.exe" -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Dfile.encoding=utf-8 -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'
    global proc
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    line = proc.stdout.readline()
    # print(line.decode('gbk'))
    line = proc.stdout.readline()
    # print(line.decode('gbk'))
    line = proc.stdout.readline()
    # print(line.decode('gbk'))
    line = proc.stdout.readline()
    # print(line.decode('gbk'))
    line = proc.stdout.readline()
    # print(line.decode('gbk'))

    msg = 'cont\r\n'.encode('utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()

    outthr.setDaemon(True)
    outthr.start()

    inthr.setDaemon(True)
    inthr.start()

    msg = 'exclude org.loushang.sca.*,flex.*,com.alibaba.*,org.springframework.*,com.fasterxml.*,com.mysql.*,com.mchange.*,net.*,org.codehaus.*,org.mybatis.*,com.microsoft.*,org.apache.*,java.*,sun.*,javax.*,com.sun.*,org.json.*,org.xml.*,edu.emory.*\r\n'.encode(
        'utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()

    #  org.loushang.sca.*,com.alibaba.druid.*,org.springframework.*,com.fasterxml.*,com.mysql.*,com.mchange.*,net.*,org.codehaus.*,org.mybatis.*,org.loushang.*,
    '''
    msg = 'trace go methods exit\r\n'.encode('utf-8')
    process1.stdin.write(msg)
    process1.stdin.flush()
    '''
    outthr.join()
    inthr.join()


if __name__ == '__main__':
    main()
