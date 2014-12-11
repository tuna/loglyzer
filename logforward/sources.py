#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import threading


def _LogPipe(collector, forwarder):
    forwarder.register(collector.cname)
    collector.follow(forwarder.process_line)


def LogSource(collector, forwarder):
    t = threading.Thread(target=_LogPipe, args=(collector, forwarder))
    t.setDaemon(True)
    t.start()
    return t


# vim: ts=4 sw=4 sts=4 expandtab
