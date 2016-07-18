
import time
from asynchronizer import asynchronize, startPool, setWorkers

setWorkers(7)

@asynchronize
def func(i,a):
    print a,i
    if i*100 < 1000:
        func(i*100,'lopp',priority=0)
    time.sleep(1)


for i in range(1,10):
    func(i,'loop')

startPool()
