#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sh
from datetime import datetime


class BaseCollector(object):

    def follow(self, process_line_func):
        raise NotImplemented("Implement this!")


class FileCollector(BaseCollector):

    def __init__(self, cname, filename):
        self.cname = cname
        self.filename = filename

    def follow(self, process_line_func):
        def ignore(*args):
            pass

        def _process(line):
            return process_line_func({
                'name': self.cname,
                'msg': line,
                'pid': None,
                't': datetime.now()
            })

        p = sh.tail('--follow=name', '-q', '--lines=0', self.filename,
                    _out=_process, _err=ignore)
        p.wait()


class SystemdJournalCollector(BaseCollector):

    def __init__(self, cname, unitname):
        import systemd.journal
        self.cname = cname
        self.unitname = unitname
        self.reader = systemd.journal.Reader()
        self.reader.this_boot()
        self.reader.log_level(systemd.journal.LOG_INFO)
        self.reader.add_match(_SYSTEMD_UNIT=self.unitname)

    def follow(self, process_line_func):
        now = datetime.now()
        self.reader.seek_realtime(now)
        while 1:
            self.reader.wait()
            for line in self.reader:
                process_line_func({
                    'name': self.cname,
                    't': line['__REALTIME_TIMESTAMP'],
                    'pid': line['_PID'],
                    'msg': line['MESSAGE']
                })


# vim: ts=4 sw=4 sts=4 expandtab
