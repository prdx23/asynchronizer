from gevent import monkey
monkey.patch_all()

import gevent.pool
import gevent.queue
import gevent
import time


class asynchronizer():
    def __init__(self,workers=32):
        self.workers = workers
        self.pool = gevent.pool.Pool(self.workers)
        self.pqueue = gevent.queue.PriorityQueue()

    def add(self,priority,func,*args,**kwargs):
        self.pqueue.put_nowait((priority,func,args,kwargs))

    def run(self):
        while not self.pqueue.empty() and not self.pool.full():
            for x in xrange(0, min(self.pqueue.qsize(), self.pool.free_count())):
                t = self.pqueue.get_nowait()
                self.pool.start(self.pool.spawn(t[1],*t[2],**t[3]))
            self.pool.join()


def asynchronize(func):
    def converted_func(*args,**kwargs):
        priority = kwargs['priority']  if 'priority' in kwargs else 1

        if 'priority' in kwargs: del kwargs['priority']
        if 'func' in kwargs: del kwargs['func']

        a.add(priority,func,*args,**kwargs)
    return converted_func


a = asynchronizer(5)

@asynchronize
def func(i):
    print 'loop',i
    if i*100 < 1000:
        func(i*100,priority=0)
    time.sleep(1)


for i in range(1,10):
    func(i)

a.run()
