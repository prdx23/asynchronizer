# -*- coding: utf-8 -*-
import multiprocessing
import time


class Actor(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.inbox, self.pipe = multiprocessing.Pipe()
        self.start()

    def run(self):
        while True:
            try:
                item = self.pipe.recv()
                if item is None:
                    break
                self.recieve(item)

            except EOFError:
                break
        self.inbox.close()
        self.pipe.close()

    def recieve(self, item):
        raise NotImplementedError
        time.sleep(0.5)
        print self.name, 'recieved', item
        time.sleep(0.5)


processes = []
for i in range(5):
    p = Actor()
    processes.append(p)


for proc in processes:
    for i in range(5):
        proc.inbox.send(i)
    print 'send'

for proc in processes:
    proc.inbox.send(None)

for proc in processes:
    proc.join()
