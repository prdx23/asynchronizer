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
        print self.name, 'recieved', item
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


class Asynchronizer():

    def __init__(self, max_processes=None, skip_mp=False):
        if max_processes is None:
            try:
                self.max_processes = multiprocessing.cpu_count()
            except:
                self.max_processes = 4
        elif skip_mp is True:
            self.max_processes = 1
        else:
            self.max_processes = max_processes
        self.function_queue = multiprocessing.Queue()
        self.processes = []

    def spawn_processes(self, item):
        if len(self.processes) < self.max_processes:
            s = Subprocess()
            s.inbox.send(item)
            self.processes.append(s)
            return

        amounts = [x.proc_amount for x in self.processes]
        print amounts
        indexes = [x[0] for x in enumerate(amounts) if x[1] == min(amounts)]
        self.processes[indexes[0]].inbox.send(item)

    def wait(self):
        for proc in self.processes:
            proc.join()

    def end(self):
        for proc in self.processes:
            proc.inbox.send(None)
        for proc in self.processes:
            proc.join()
