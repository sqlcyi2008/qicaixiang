#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

'''
把qicai_app服务打包成C:\Python27\Scripts下的exe文件
'''

setup(
    name="qicaixiang",  #pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    version="1.0",
    author="lichuanyi",
    author_email="123438115@qq.com",
    description=(""),
    license="GPLv3",
    keywords="",
    url="",
    packages=['RedisRun'],  # 需要打包的目录列表

    # 需要安装的依赖
    install_requires=[
        'tornado>=4.5.2',
        'dpkt>=1.9.1',
        'psutil>=5.3.1',
        'redis>=2.10.5',
        'setuptools>=16.0',
    ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'qicai_app_run = RedisRun.qicai_app_run:main',
    ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)