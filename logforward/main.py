#!/usr/bin/env python2.7
# -*- coding:utf8 -*-
from collector import SystemdJournalCollector, FileCollector
from forwarder import RedisForwarder
from sources import LogSource

import settings


def main():

    collectors = []

    for cname, log_source in settings.LOG_SOURCES:
        if log_source['type'] == "file":
            collectors.append(FileCollector(cname, log_source['filename']))
        elif log_source['type'] == "systemd-journal":
            collectors.append(
                SystemdJournalCollector(cname, log_source['unitname']))

    f = RedisForwarder(
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        settings.REDIS_DB,
        settings.REDIS_PREFIX)

    threads = [LogSource(c, f) for c in collectors]
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
