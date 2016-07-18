from gevent import monkey
monkey.patch_all()

import gevent.pool
import gevent.queue
import gevent
import time
import requests

max_workers = 5
pool = gevent.pool.Pool(max_workers)
queue = gevent.queue.Queue()


def func(i):

    print 'loop',i
    queue.put_nowait((func,i*100))
    time.sleep(1)


for i in range(10):
    queue.put_nowait((func,i))



while not queue.empty() and not pool.full():
    for x in xrange(0, min(queue.qsize(), pool.free_count())):
        t = queue.get_nowait()
        pool.start(pool.spawn(t[0],t[1]))
    pool.join()