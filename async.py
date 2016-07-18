from gevent import monkey
monkey.patch_all()

import gevent.pool
import gevent.queue
import gevent
import time
import requests

max_workers = 5
pool = gevent.pool.Pool(max_workers)
queue = gevent.queue.PriorityQueue()


def func(i):
    print 'loop',i
    if i*100 < 1000:
        queue.put_nowait((0,func,i*100))
    time.sleep(1)


for i in range(1,10):
    queue.put_nowait((1,func,i))



while not queue.empty() and not pool.full():
    for x in xrange(0, min(queue.qsize(), pool.free_count())):
        t = queue.get_nowait()
        pool.start(pool.spawn(t[1],t[2]))
    pool.join()
