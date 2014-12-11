#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import redis
import json
from datetime import datetime


class RedisReceiver(object):

    def __init__(self, host, port, db, prefix):
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        self._prefix = prefix
        self.channels = {}

    def register(self, cname, processor):
        if cname not in self.channels:
            self.channels[cname] = [processor, ]
        else:
            self.channels[cname].append(processor)

    def poll(self):
        keys = [self._prefix + "buf_" + k for k in self.channels]
        while 1:
            cname, jmsg = self.r.blpop(keys)
            msg = json.loads(jmsg)
            msg['t'] = datetime.fromtimestamp(float(msg['t']))

            if cname not in self.channels:
                continue
            for p in self.channels[cname]:
                p.push(msg)


# vim: ts=4 sw=4 sts=4 expandtab
