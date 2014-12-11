#!/usr/bin/env python2
from datetime import datetime, timedelta
from settings import LOG_FILE_FORMAT, IPADDR_TYPE
import ipaddr
import logging
import re

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.WARN)


class AccessHit(object):
    # raw_log      # string: raw original log
    # date_time    # datetime: for access time
    # subdirectory # string: accessed subdirectory, eg '/ubuntu'
    # bytes_sent   # string: transferred file size, in bytes
    # ip_addr      # ipaddress: accessed IP
    # ip_type      # string: type of accessed IP, eg 'tsinghua-ipv6'
    _compiled_log_re = re.compile(LOG_FILE_FORMAT['log_format'])
    _compiled_request_re = re.compile(r'^(?P<method>[^ ]*) (?P<subdirectory>/[^/ ]*)/?[^ ]* (?P<protocol>.*)$')
    _thu_ip_network = {t: [ipaddr.IPNetwork(n) for n in subnets]
                       for t, subnets in IPADDR_TYPE.items()}

    __slots__ = ('raw_log', 'ip_addr', 'date_time', 'subdirectory', 'bytes_sent', 'ip_type')

    def __init__(self, log_str=None):
        self.raw_log = log_str
        matched = AccessHit._log_to_matched(log_str)
        if not matched:
            return
        try:
            self.ip_addr = ipaddr.IPAddress(matched.group('remote_addr'))
            self.ip_addr = ipaddr.IPAddress(matched.group('http_x_forwarded_for'))
        except ValueError:
            pass
        self.date_time = AccessHit._parse_time(matched.group('time_local'))
        self.subdirectory = AccessHit._request_to_subdirectory(matched.group('request'))
        self.bytes_sent = int(matched.group('body_bytes_sent'))
        self.ip_type = AccessHit._ip_type_detection(self.ip_addr)

    def __str__(self):
        if self.ip_type:
            return str(self.ip_addr) + ' is ' + str(self.ip_type)
        else:
            return ''

    @classmethod
    def _parse_time(cls, timestr):
        offset = int(timestr[-5:])
        delta = timedelta(hours=offset/100)
        t = datetime.strptime(timestr[:-6], LOG_FILE_FORMAT['time_format_notz'])
        return t - delta

    @classmethod
    def _log_to_matched(cls, log_str):
        matched = AccessHit._compiled_log_re.match(log_str)
        if not matched:
            logger.warning('AccessHit: log not not recognized')
            logger.warning(log_str)
            return None
        else:
            logger.debug('AccessHit: new log detected')
            logger.debug('raw_log=' + log_str)
            logger.debug('remote_addr=' + matched.group('remote_addr'))
            logger.debug('timelocal=' + matched.group('time_local'))
            logger.debug('request=' + matched.group('request'))
            logger.debug('body_bytes_sent=' + matched.group('body_bytes_sent'))
            logger.debug('http_x_forwarded_for=' + matched.group('http_x_forwarded_for'))
            return matched

    @classmethod
    def _request_to_subdirectory(cls, request):
        # e.g. GET /ubuntu/dists/precise/main/binary-i386/Packages.bz2 HTTP/1.1
        # TODO: subsubdirectory supports?
        matched = AccessHit._compiled_request_re.match(request)
        if not matched:
            logger.debug('AccessHit: request not not recognized')
            logger.debug(request)
            return None
        else:
            subdirectory = matched.group('subdirectory')
            if ':' in subdirectory:  # e.g. GET http://www.baidu.com/ HTTP/1.1
                logger.debug('AccessHit: a proxy request')
                logger.debug(request)
                return None
            return subdirectory

    @classmethod
    def _ip_type_detection(cls, ip_addr):
        for ip_type, subnets in AccessHit._thu_ip_network.items():
            for subnet in subnets:
                if ip_addr in subnet:
                    return ip_type

        return 'other-ipv' + str(ip_addr.version)


def test():
    print('not implemented')

if __name__ == '__main__':
    test()
