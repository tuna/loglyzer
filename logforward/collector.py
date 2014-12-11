#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sh
import json
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
        self.cname = cname
        self.unitname = unitname

    def follow(self, process_line_func):
        def ignore(*args):
            pass

        def _process(line):
            msg = json.loads(line)
            return process_line_func({
                'name': self.cname,
                't': msg['__REALTIME_TIMESTAMP'],
                'pid': msg['_PID'],
                'msg': msg['MESSAGE']
            })
            p = sh.journalctl('-f', '--lines=0', '--output=json',
                              '-u', self.unitname, _out=_process, _err=ignore)
            p.wait()


# vim: ts=4 sw=4 sts=4 expandtab
