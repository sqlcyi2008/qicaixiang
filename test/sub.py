# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import zipfile

z = zipfile.ZipFile('D:/apps/apache-tomcat-7.0.72/webapps/loushang/WEB-INF/lib/spring.jar', 'r')
print(len(z.filelist))
for i in z.namelist():
    print(i)

print(z.read('org/springframework/web/util/WebUtils.class'))