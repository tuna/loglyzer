#!/usr/bin/env python2.7
# -*- coding:utf8 -*-
import sh


def process_line(line):
    print(line)


def ignore(line):
    pass


def main(log_file='/var/log/nginx/access.log'):
    p = sh.tail('--follow=name', '-q', '--lines=0', log_file,
                _out=process_line, _err=ignore)
    p.wait()


if __name__ == "__main__":
    main()
