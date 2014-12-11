#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()

import settings
from receiver import RedisReceiver
from archiver import LogArchiver


def main():
    r = RedisReceiver(
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        settings.REDIS_DB,
        settings.REDIS_FWD_PREFIX)

    for cname, processors in settings.LOG_PROCESSORS.items():
        for p in processors:
            t = p.pop('type')
            if t == "archive":
                a = LogArchiver(cname, **p)
                r.register(cname, a)

    r.poll()

if __name__ == "__main__":
    main()

# vim: ts=4 sw=4 sts=4 expandtab
