# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def main():
    os.system('"C:/Program Files/Java/jdk1.8.0_121/bin/java.exe"   -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:/apps/apache-tomcat-7.0.72/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Dfile.encoding=utf-8   -Djava.endorsed.dirs=D:/apps/apache-tomcat-7.0.72/endorsed -classpath D:/apps/apache-tomcat-7.0.72/bin/bootstrap.jar;D:/apps/apache-tomcat-7.0.72/bin/tomcat-juli.jar -Dcatalina.base=D:/apps/apache-tomcat-7.0.72 -Dcatalina.home=D:/apps/apache-tomcat-7.0.72 -Djava.io.tmpdir=D:/apps/apache-tomcat-7.0.72/temp org.apache.catalina.startup.Bootstrap  start')


if __name__ == '__main__':
    main()
