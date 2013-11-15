#!/usr/bin/python3

# Estimates time spent on a project from commit timestamps
#
# If two commits are less than INERTIA time apart, the time
# between them is considered spent, otherwise SINGLE_COMMIT
# time is taken.

import os
import sys
from datetime import timedelta, datetime

STATS="~/scripts/stats.py"
FORMAT="%Y-%m-%d"

SINGLE_COMMIT=1800 # 30 min
INERTIA=7200 # 2 h
DELTA=timedelta(days=7)
BEGIN=datetime.strptime("2013-01-01", FORMAT)

begin = BEGIN
now = datetime.now()

table = dict()
users = set()
times = set()

while begin < now:
    end = begin + DELTA
    data = os.popen(STATS + " --since {} --until {}".format(begin.strftime(FORMAT), end.strftime(FORMAT)) + ' ' + ' '.join(sys.argv[1:]))
    data = list(data)
    for line in data[1:]:
        user, hours = line.strip().split("\t")[:2]

        users.add(user)
        times.add(begin)
        if user not in table:
            table[user] = dict()
        if begin not in table[user]:
            table[user][begin] = 0
        table[user][begin] += float(hours)
    begin += DELTA

print("user", end='')
for time in sorted(times):
    print(";{}".format(time.strftime(FORMAT)), end='')
print()

for user in users:
    print(user, end='')
    for time in sorted(times):
        if time in table[user]:
            print(";{}".format(table[user][time]), end='')
        else:
            print(";", end='')
    print()

