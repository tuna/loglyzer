#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import json
import redis


class BaseForwarder(object):

    def register(self, cname):
        raise NotImplemented("Implement this!")

    def process_line(self, line):
        raise NotImplemented("Implement this!")


class StdOutForwarder(BaseForwarder):
    ''' for testing purpose'''
    def process_line(self, line):
        print(line)

    def register(self, cname):
        pass


class RedisForwarder(BaseForwarder):

    def __init__(self, host, port, db, prefix):
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        self._prefix = prefix
        self.r.delete(prefix+"collectors")

    def register(self, cname):
        self.r.sadd(self._prefix+"collectors", cname)
        self.r.publish(self._prefix+"events", "NEW_COLLECTOR")

    def process_line(self, line):
        cname = line['name']
        buf = self._prefix + "buf_" + cname
        line['t'] = float(line['t'].strftime("%s.%f"))

        self.r.rpush(buf, json.dumps(line))

# vim: ts=4 sw=4 sts=4 expandtab
