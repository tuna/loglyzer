#!/usr/bin/env python2

from access_hit import AccessHit
from settings import OUTPUT_INFO
import sys


def get_category(log, category_names):
    log_category = [
        getattr(log, cn, None) or None for cn in category_names
    ]
    if None in log_category:
        return None
    return tuple(log_category)


def unique_logs(logs, unique_attr):
    seen = set()
    return [x for x in logs
            if not (getattr(x, unique_attr) in seen
                    or seen.add(getattr(x, unique_attr)))]


def app():
    logs = [AccessHit(line) for line in sys.stdin]

    for output in OUTPUT_INFO:
        print('--------' + output + '--------')
        categorized_logs = {}
        for log in logs:
            category = get_category(log, OUTPUT_INFO[output]['category'])
            if not category:
                continue
            if category not in categorized_logs:
                categorized_logs[category] = []
            categorized_logs[category].append(log)

        categorized_value = []

        for category, cate_logs in categorized_logs.items():
            value = 0
            for unique in OUTPUT_INFO[output]['unique']:
                cate_logs = unique_logs(cate_logs, unique)

            for log in cate_logs:
                if isinstance(OUTPUT_INFO[output]['weight'], basestring):
                    value += getattr(log, OUTPUT_INFO[output]['weight'])
                else:
                    value += OUTPUT_INFO[output]['weight']
            categorized_value.append((value, category))

        for category in reversed(sorted(categorized_value)):
            print("{}:{}".format(*category[::-1]))

if __name__ == '__main__':
    app()
