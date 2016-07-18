
import time
from async import asynchronize, startPool, setWorkers

setWorkers(5)

@asynchronize
def func(i):
    print 'loop',i
    if i*100 < 1000:
        func(i*100,priority=0)
    time.sleep(1)


for i in range(1,10):
    func(i)

startPool()
