#!/usr/bin/env python2

LOG_FILE_FORMAT = {
    'log_format': r'^(?P<remote_addr>[0-9a-f.:]*) - (?P<remote_user>[^ ]*) \[(?P<time_local>[^]]*)\] "(?P<request>[^"]*)" (?P<status>\d*) (?P<body_bytes_sent>\d*) "(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)" "(?P<http_x_forwarded_for>[^"]*)"$',
    'time_format': '%d/%b/%Y:%H:%M:%S %z',
    'time_format_notz': '%d/%b/%Y:%H:%M:%S',
    # e.g 09/Dec/2014:06:30:20 +0800
}

IPADDR_TYPE = {
    'tsinghua-ipv4': [
        '166.111.0.0/16',
    ],
    'tsinghua-ipv6': [
        '2402:f000::/32',
    ],
}

OUTPUT_INFO = {
    'subdirectory-bytes': {
        'category': [
            'subdirectory',
        ],
        'unique': [],
        'weight': 'bytes_sent',
    },
    'ip-type-bytes': {
        'category': [
            'ip_type',
        ],
        'unique': [],
        'weight': 'bytes_sent',
    },
    'subdirectory-unique-ip': {
        'category': [
            'subdirectory',
        ],
        'unique': [
            'ip_addr',
        ],
        'weight': 1,
    },
    'ip-type-unique-ip': {
        'category': [
            'ip_type',
        ],
        'unique': [
            'ip_addr',
        ],
        'weight': 1,
    },
    'subdirectory-ip-type-unique-ip': {
        'category': [
            'subdirectory',
            'ip_type',
        ],
        'unique': [
            'ip_addr',
        ],
        'weight': 1,
    },
}

try:
    from settings_local import *
except:
    pass
