import queue
import threading
from urllib.request import urlopen
import requests

def get_urls():
    res = []
    with open("url_lists.txt", "r")  as f:
        lines = f.readlines()
        for n, l in enumerate(lines):
            
            try:
                s = "http://"
                s += l.split()[1].rstrip()
                if any(i in s for i in ["google", "blogspot"]):
                    continue
                res.append(s)
            except:
                pass
    return res

def get_request(q, urls, requests_session):
    try:
        res = requests_session.get(urls, timeout=3)
        q.put(res)
    except:
         q.put(None)
urls = []

urls = get_urls()


import time
start_time = time.time()
q = queue.Queue()
requests_session= requests.Session()

# for u in urls:
#     t = threading.Thread(target=get_request, args = (q,u, requests_session))
#     t.daemon = True
#     t.start()


res = []
for i in urls:
    res.append(q.get())
l = [i for i in res if i]
print (len(l))
#print(res)
print("--- %s seconds ---" % (time.time() - start_time))
