#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import os
import gzip
# import datetime

import gevent
from gevent.queue import Queue
from gevent.fileobject import FileObject
from gevent.threadpool import ThreadPool
from log_processor import BaseLogProcessor


class LogArchiver(BaseLogProcessor):

    pool = ThreadPool(3)

    def __init__(self, cname, local_dir):
        self.cname = cname
        self.local_dir = local_dir
        self.f = None

        self._cur_date = None

        self._aof_file = os.path.join(
            self.local_dir, "LOG")
        self._tmp_file = os.path.join(
            self.local_dir, "TMP")
        self._gz_tmpl = os.path.join(
            self.local_dir, self.cname + "_{date}.gz")

        self._open_log()
        self.queue = Queue()
        gevent.spawn(self._write_log)

    def _open_log(self):
        self.f = FileObject(open(self._aof_file, 'a+'), 'a+')

    def compress(self, date):
        self.f.close()
        os.rename(self._aof_file, self._tmp_file)
        LogArchiver.pool.spawn(self._compress, date)
        self._open_log()

    def _compress(self, date):
        f_in = open(self._tmp_file, 'rb')
        filename = self._gz_tmpl.format(date=date)
        gz = gzip.open(filename, 'wb')
        gz.writelines(f_in)
        gz.close()
        f_in.close()

    @classmethod
    def join(cls):
        cls.pool.join()

    def _write_log(self):
        while 1:
            entry = self.queue.get()
            date = entry['t'].date()

            if self._cur_date is None:
                self._cur_date = entry['t'].date()

            if date > self._cur_date:
                self.compress(self._cur_date.strftime("%Y-%m-%d"))
                self._cur_date = date

            self.f.write(entry['msg'])
            if not entry['msg'].endswith('\n'):
                self.f.write('\n')
            self.f.flush()

    def push(self, entry):
        self.queue.put(entry)

# vim: ts=4 sw=4 sts=4 expandtab
