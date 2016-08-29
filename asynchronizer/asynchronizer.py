# -*- coding: utf-8 -*-
import multiprocessing

import gevent.pool
import gevent.queue
from gevent import monkey
monkey.patch_all()


class Actor(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.inbox, self.pipe = multiprocessing.Pipe()

    def run(self):
        while True:
            try:
                item = self.pipe.recv()
                self.recieve(item)
                if item is None:
                    break
            except EOFError:
                break

        self.inbox.close()
        self.pipe.close()

    def recieve(self, item):
        raise NotImplementedError


class Subprocess(Actor):

    def __init__(self, max_workers=4, skip_gevent=False):
        Actor.__init__(self)
        self.max_workers = max_workers
        self.skip_gevent = skip_gevent
        self.pool = gevent.pool.Pool(max_workers)
        self.p_queue = gevent.queue.PriorityQueue()
        self.proc_amount = 0
        self.start()

    def worker(self):
        while True:
            try:
                p, func, args, kwargs = self.p_queue.get_nowait()
                func(*args, **kwargs)
                self.proc_amount -= 1
            except gevent.queue.Empty:
                break

    def recieve(self, item):
        self.proc_amount += 1

        if self.skip_gevent is True:
            if item is None:
                return
            p, func, args, kwargs = item
            func(*args, **kwargs)
            self.proc_amount -= 1
            return

        if item is None:
            self.pool.join()
            return

        self.p_queue.put_nowait(item)
        for x in range(0, min(self.p_queue.qsize(), self.pool.free_count())):
            self.pool.spawn(self.worker)
