# -*- coding: utf-8 -*-
import multiprocessing


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
