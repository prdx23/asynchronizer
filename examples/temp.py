# -*- coding: utf-8 -*-
# import time
from datetime import datetime

import requests

import asynchronizer
from asynchronizer import asynchronize

start_time = datetime.now()
s = requests.session()


@asynchronize
def func(i, j):
    try:
        r = s.get('https://httpbin.org/get')
        status = r.status_code
    except requests.exceptions.ConnectionError:
        status = 'Connection refused'

    print 'Processed i[%d] j[%d]  result - %s' % (i, j, status)


def run_only_mp():
    start_time = datetime.now()
    print 'Running only multiprocessing :'
    asynchronizer.config(skip_gevent=True)
    asynchronizer.config(processes=16)
    for i in range(25):
        for j in range(4):
            func(i, j)
    asynchronizer.end()
    print 'Total time for multiprocessing : %s' % \
        (datetime.now() - start_time)


def run_only_gevent():
    start_time = datetime.now()
    print 'Running only gevent :'
    asynchronizer.config(skip_mp=True, skip_gevent=False)
    asynchronizer.config(workers=16)
    for i in range(25):
        for j in range(4):
            func(i, j)
    asynchronizer.end()
    print 'Total time for gevent : %s' % \
        (datetime.now() - start_time)


def run_asynchronizer():
    start_time = datetime.now()
    print 'Running asnchronizer (combo of multiprocessing and gevent) :'
    asynchronizer.config(skip_gevent=False, skip_mp=False)
    asynchronizer.config(processes=4, workers=4)
    for i in range(25):
        for j in range(4):
            func(i, j)
    asynchronizer.end()
    print 'Total time for asynchronizer : %s' % \
        (datetime.now() - start_time)


# run_only_mp()
# run_only_gevent()
run_asynchronizer()
