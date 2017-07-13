__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

import urllib3
import re
http = urllib3.PoolManager()
response = http.request('GET', 'http://192.168.0.36:5000/video_feed')
print(type(response.data))
btemp = bytearray(response.data)
m = re.search( "\xff\xd8", btemp.decode('ISO-8859-1'))
a = m.start()
m1 = re.search("\xff\xd9", btemp.decode('ISO-8859-1'))
b = m1.start()
if a != -1 and b != -1:
    jpg1 = btemp[a:b + 2]


with open("/tmp/frame.jpg", "wb") as f:
    f.write(jpg1)