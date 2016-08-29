# -*- coding: utf-8 -*-
import time
from datetime import datetime

from asynchronizer import Subprocess

start_time = datetime.now()


def func(item):
    time.sleep(0.5)
    print 'processed', item
    time.sleep(0.5)

processes = []
for i in range(5):
    p = Subprocess()
    processes.append(p)

j = 0
for proc in processes:
    for i in range(5):
        t = (1, func, [str(j) + str(i)], {})
        proc.inbox.send(t)
    print 'send'
    j += 1

for proc in processes:
    proc.inbox.send(None)

for proc in processes:
    proc.join()

print 'Total time : %s' % (datetime.now() - start_time)
