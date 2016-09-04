# -*- coding: utf-8 -*-
import multiprocessing
from functools import wraps

import dill
import gevent.pool
import gevent.queue
from gevent import monkey
monkey.patch_all()

default_w = 4
default_sp = 4


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
                # TODO : mention the gevent-mp socket pipe problem
                continue

        self.inbox.close()
        self.pipe.close()

    def recieve(self, item):
        raise NotImplementedError


class Subprocess(Actor):

    def __init__(self, max_workers=default_w, skip_gevent=False):
        Actor.__init__(self)
        self.max_workers = max_workers
        self.skip_gevent = skip_gevent
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
        if self.skip_gevent is True:
            if item is None:
                return
            p, pickled_func, args, kwargs = item
            func = dill.loads(pickled_func)
            func(*args, **kwargs)
            return

        if item is None:
            self.pool.join()
            return

        self.p_queue.put_nowait(item)
        for x in range(0, min(self.p_queue.qsize(), self.pool.free_count())):
            self.pool.spawn(self.worker)


class Asynchronizer():

    def __init__(self,
                 max_processes=None, skip_mp=False, max_w=None, skip_g=None):
        if max_processes is None and skip_mp is False:
            try:
                self.max_processes = multiprocessing.cpu_count()
            except:
                self.max_processes = default_sp
        elif skip_mp is True:
            self.max_processes = 1
        else:
            self.max_processes = max_processes
        self.processes = []
        self.p = 0
        # TODO : fix naming of these
        self.max_w = max_w if max_w is not None else default_w
        self.skip_g = skip_g

    def spawn_processes(self, priority, pickled_func, args, kwargs):
        item = (priority, pickled_func, args, kwargs)

        if len(self.processes) < self.max_processes:
            if self.skip_g is False:
                s = Subprocess(max_workers=self.max_w, skip_gevent=False)
            else:
                s = Subprocess(max_workers=self.max_w, skip_gevent=True)
            s.inbox.send(item)
            self.processes.append(s)
            return

        # TODO : optimize this, evenly distribute
        # TODO : add check for crashed processes
        self.p = (self.p + 1) % self.max_processes
        self.processes[self.p].inbox.send(item)

    def wait_async(self):
        for proc in self.processes:
            proc.join()

    def end_async(self):
        for proc in self.processes:
            proc.inbox.send(None)
        for proc in self.processes:
            proc.join()


a = Asynchronizer(skip_mp=False)
# TODO : func for custom workers/subprocesses


def asynchronize(async_func):
    @wraps(async_func)
    def converted_func(*args, **kwargs):
        # TODO : error handling
        pickled_func = dill.dumps(async_func)
        a.spawn_processes(1, pickled_func, args, kwargs)
    return converted_func


def end_async():
    a.end_async()


def config_async(
        processes=None, greenlets=None, skip_mp=False, skip_gevent=False):

    if processes is not None:
        a.max_processes = processes if processes > 0 else 1

    if greenlets is not None:
        if greenlets > 0:
            a.max_w = greenlets
        else:
            a.skip_g = True

    if skip_mp is True:
        a.max_processes = 1

    if skip_gevent is True:
        a.skip_g = True
