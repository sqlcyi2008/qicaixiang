# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
from watchdog.observers import Observer
from watchdog.events import *
from qi.plugins.utils import *


class QiCaiHandler(FileSystemEventHandler):
    def on_created(self, event):
        # print("file %s created!" % event.src_path)
        line = "file %s created!" % event.src_path
        write_redis("file->" + line)

    def on_modified(self, event):
        # print("file %s modified!" % event.src_path)
        line = "file %s modified!" % event.src_path
        write_redis("file->" + line)

    def on_deleted(self, event):
        # print("file %s deleted!" % event.src_path)
        line = "file %s deleted!" % event.src_path
        write_redis("file->" + line)


if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = QiCaiHandler()

    observer = Observer()
    path = "d:\\"
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
