'''
This script will take 55 seconds to run normally,
but only 10 seconds when run asynchronously
'''

# To run:
# pip install asynchronizer
import time
from asynchronizer import asynchronize, startPool, setWorkers

# try commenting this decorater to see the effect
@asynchronize
def func(i):
    time.sleep(i)
    print i

for i in range(1,11):
    func(i)

startPool()
