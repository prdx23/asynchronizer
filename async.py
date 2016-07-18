from gevent import monkey
monkey.patch_all()

import gevent.pool
import gevent.queue
import gevent
import time
# import requests
#
# max_workers = 5
# pool = gevent.pool.Pool(max_workers)
# queue = gevent.queue.PriorityQueue()


class asynchronizer():

    def __init__(self,workers=32):
        self.workers = workers
        self.pool = gevent.pool.Pool(self.workers)
        self.pqueue = gevent.queue.PriorityQueue()

    def add(self,priority,func,params):
        self.pqueue.put_nowait((priority,func,params))

    def run(self):
        while not self.pqueue.empty() and not self.pool.full():
            for x in xrange(0, min(self.pqueue.qsize(), self.pool.free_count())):
                t = self.pqueue.get_nowait()
                self.pool.start(self.pool.spawn(t[1],t[2]))
            self.pool.join()


a = asynchronizer(5)


def func(i):
    print 'loop',i
    if i*100 < 1000:
        a.add(0,func,i*100)
    time.sleep(1)


for i in range(1,10):
    a.add(1,func,i)


a.run()

#
#
# while not queue.empty() and not pool.full():
#     for x in xrange(0, min(queue.qsize(), pool.free_count())):
#         t = queue.get_nowait()
#         pool.start(pool.spawn(t[1],t[2]))
#     pool.join()
