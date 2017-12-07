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


# jdb子进程
global proc


def outThread(var):
    while True:
        global proc
        line = proc.stdout.readline()
        if not line:
            break
        line = line.decode('gbk')
        # print(line)
        write_redis("code->" + line)
        if 'Server startup in' in line:
            #msg = 'trace go methods\r\n'.encode('utf-8')
            msg = 'stop at com.inspur.sw.stpptnr.cmd.StPptnRCommand:706\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()

        if '断点命中:' in line:
            msg = 'locals\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()

            msg = 'cont\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()


def formatCmd(line):
    line=line[line.find('->')+2:].replace('\\','/')
    java = "\""+line[:line.find('java.exe') + 8].replace('java.exe','jdb.exe')+"\""
    options = line[line.find('java.exe') + 8:]
    return java+" -launch "+options

def main():
    outthr = threading.Thread(target=outThread, args=(u'输出线程',))

    global r
    line = r.get(constants.QI_JAVA_CMDLINE)

    command = formatCmd(line.decode(encoding="utf-8", errors="ignore"))
    print("!!!222" +command)
    # command = 'jdb.exe -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'
    # command = '"C:\\Program Files\\Java\\jdk1.8.0_121\\bin\\jdb.exe" -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Dfile.encoding=utf-8 -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'
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

    msg = 'exclude flex.*,com.microsoft.*,org.apache.*,java.*,sun.*,javax.*,org.loushang.*,com.sun.*,org.json.*,org.xml.*,edu.emory.*\r\n'.encode(
        'utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()

    '''
    msg = 'trace go methods\r\n'.encode('utf-8')
    process1.stdin.write(msg)
    process1.stdin.flush()
    '''
    outthr.join()


if __name__ == '__main__':
    main()
