#!/usr/bin/env python2
# -*- coding:utf-8 -*-


class BaseLogProcessor(object):

    def push(self, entry):
        raise NotImplemented("Not Implemented!")


# vim: ts=4 sw=4 sts=4 expandtab
