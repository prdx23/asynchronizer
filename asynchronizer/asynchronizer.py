# -*- coding: utf-8 -*-
import multiprocessing
from functools import wraps

import dill
import gevent.pool
import gevent.queue
from gevent import monkey
monkey.patch_all()

DEFAULT_W = 4
try:
    DEFAULT_SP = multiprocessing.cpu_count()
except:
    DEFAULT_SP = 4


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
            except IOError:
                # TODO : mention the gevent-mp socket pipe problem in doc
                continue

        self.inbox.close()
        self.pipe.close()

    def recieve(self, item):
        raise NotImplementedError


class Subprocess(Actor):

    def __init__(self, max_workers=DEFAULT_W):
        Actor.__init__(self)
        self.max_workers = max_workers
        self.pool = gevent.pool.Pool(max_workers)
        self.p_queue = gevent.queue.PriorityQueue()
        self.start()

    def worker(self):
        while True:
            try:
                p, pickled_func, args, kwargs = self.p_queue.get_nowait()
                func = dill.loads(pickled_func)
                func(*args, **kwargs)
            except gevent.queue.Empty:
                break

    def recieve(self, item):
        # print self.name, 'recieved function'
        if self.max_workers <= 0:
            if item is None:
                return
            p, pickled_func, args, kwargs = item
            func = dill.loads(pickled_func)
            func(*args, **kwargs)
            return

        if item is None:
            self.pool.join()

        self.p_queue.put_nowait(item)
        for x in range(0, min(self.p_queue.qsize(), self.pool.free_count())):
            self.pool.spawn(self.worker)


class Asynchronizer():

    def __init__(self):
        self.max_processes = DEFAULT_SP
        self.max_workers = DEFAULT_W
        self.counter = 0
        self.processes = []

    def set_processes_no(self, n=None, skip_mp=False):
        if skip_mp is True or n == 0:
            self.max_processes = 1  # temp , reset to 0
        elif skip_mp is False:
            self.max_processes = DEFAULT_SP if (n is None or n < 0) else n

    def set_workers_no(self, n=None, skip_gv=False):
        if skip_gv is True or n == 0:
            self.max_workers = 0
        elif skip_gv is False:
            self.max_workers = DEFAULT_W if (n is None or n < 0) else n

    def wait(self):
        for proc in self.processes:
            proc.join()

    def end(self):
        for proc in self.processes:
            proc.inbox.send(None)
        for proc in self.processes:
            proc.join()

    def spawn_processes(self, priority, func, args, kwargs):
        # TODO : error handling
        pickled_func = dill.dumps(func)
        item = (priority, pickled_func, args, kwargs)

        if len(self.processes) < self.max_processes:
            s = Subprocess(max_workers=self.max_workers)
            s.inbox.send(item)
            self.processes.append(s)
            return

        # TODO : optimize this, evenly distribute
        # TODO : add check for crashed processes
        self.counter = (self.counter + 1) % self.max_processes
        self.processes[self.counter].inbox.send(item)


a = Asynchronizer()


def asynchronize(async_func):
    @wraps(async_func)
    def converted_func(*args, **kwargs):
        a.spawn_processes(1, async_func, args, kwargs)
    return converted_func


def end():
    a.end()


def wait():
    a.wait()


def config(
        processes=None,
        workers=None,
        skip_mp=False,
        skip_gevent=False):

    if skip_mp is True:
        a.set_processes_no(skip_mp=True)
    else:
        a.set_processes_no(processes)

    if skip_gevent is True:
        a.set_workers_no(skip_gv=True)
    else:
        a.set_workers_no(workers)
