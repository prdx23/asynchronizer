from gevent import monkey
monkey.patch_all()

import gevent.pool
import gevent.queue

class asynchronizer():
    def __init__(self,workers):
        # workers define how many concurrent functions should be run
        self.workers = workers
        self.pool = gevent.pool.Pool(self.workers)
        self.pqueue = gevent.queue.PriorityQueue()

    def add(self,priority,func,*args,**kwargs):
        # this function adds other functions to the priority queue
        self.pqueue.put((priority,func,args,kwargs))
        self.startWorkers()

    def updateWorkers(self,workers):
        # can be used to update no. of workers if -
        # nothing is added to the pool yet
        self.workers = workers
        self.pool = gevent.pool.Pool(self.workers)

    def worker(self):
        # this is the worker that runs inside a greenlet thread
        # this will process the queue till there are no items left
        while True:
            try:
                p,func,args,kwargs = self.pqueue.get_nowait()
                func(*args,**kwargs)
            except gevent.queue.Empty:
                return

    def startWorkers(self):
        # this function spawns the required number of greenlet threads
        for x in range(0,min(self.pqueue.qsize(),self.pool.free_count())):
            self.pool.spawn(self.worker)

    def wait(self):
        # this function will wait for all the greenlet threads to finish
        # this is a blocking function
        self.pool.join()

a = asynchronizer(32)

def asynchronize(func):
    def converted_func(*args,**kwargs):
        priority = kwargs['priority']  if 'priority' in kwargs else 1

        # remove these two parameters , as they are used in add()
        # temporary fix
        if 'priority' in kwargs: del kwargs['priority']
        if 'func' in kwargs: del kwargs['func']

        a.add(priority,func,*args,**kwargs)
    return converted_func

def Wait():
    # wrapper for asynchronizer.wait()
    a.wait()

def setWorkers(workers):
    # wrapper for asynchronizer.updateWorkers()
    a.updateWorkers(workers)
