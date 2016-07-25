# To run:
# pip install asynchronizer lxml requests

import requests
# using lxml tree to keep the example short
from lxml import html
from asynchronizer import asynchronize, Wait, setWorkers,a

# to time this script
from datetime import datetime
startTime = datetime.now()

# to set custom number of threads
setWorkers(64)
session = requests.Session()
requests_made = 0
total_requests = 0

# try commenting this decorator out, and notice the effect on the speed
@asynchronize
def extract_title(url):
    global requests_made,total_requests

    r = session.get('https://en.wikipedia.org'+url)
    tree = html.fromstring(r.text)
    try:
        title = tree.xpath('//*[@id="firstHeading"]/text()')[0]
        requests_made += 1
        print 'Requests made: ',requests_made,'/',total_requests,\
        '  Title extracted :',title,'from url',url
    except Exception as e:
        print 'Error parsing url :',url
        total_requests -= 1

# To populate the initial list of urls
r = session.get('https://en.wikipedia.org/wiki/Python_(programming_language)')
tree = html.fromstring(r.text)

# Extract href from all 'a' tags in the div with id 'mw-content-text'
l=[x.xpath('.//@href')[0] for x in tree.xpath('//*[@id="mw-content-text"]//a')]

for url in l:
    # Just a little cleaning to remove invalid urls
    if (':' not in url) and (url[0:6] == '/wiki/' and url[-4:-3] != '.'):
        extract_title(url)
        total_requests += 1

Wait()
# Output the total excecution time
print 'Total Excecution time: ',(datetime.now() - startTime)
