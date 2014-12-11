#!/usr/bin/env python2
# -*- coding:utf-8 -*-

REDIS_HOST = ""
REDIS_PORT = 6379
REDIS_DB = 0

REDIS_PREFIX = "lgr_"

try:
    from settings_local import *
except:
    pass

# vim: ts=4 sw=4 sts=4 expandtab
