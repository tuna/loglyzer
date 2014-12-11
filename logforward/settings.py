#!/usr/bin/env python2
# -*- coding:utf-8 -*-

REDIS_HOST = ""
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_PREFIX = "lgfwd_"

LOG_SOURCES = {
    'nginx': {
        'type': "file",
        "filename": "/var/log/nginx/access.log",
    },
    'rsync': {
        'type': "systemd-journal",
        "unitname": "rsync.service",
    }
}


try:
    from settings_local import *
except:
    pass

# vim: ts=4 sw=4 sts=4 expandtab
