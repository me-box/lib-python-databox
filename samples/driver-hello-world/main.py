__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

import lib as databox
import urllib3
import os
import json
from flask import Flask
import ssl
from lib.core_store import NewKeyValueClient as nkvClient
from lib.core_store import NewTimeSeriesClient as ntsClient

store= os.environ['DATABOX_STORE_ENDPOINT']
zmq_end_point= os.environ['DATABOX_ZMQ_ENDPOINT']
hostname = os.environ['DATABOX_LOCAL_NAME']

dpem = open("/run/secrets/DATABOX_PEM").read()
HTTPS_SECRETS = json.loads(dpem)
fp_cert = open(os.path.abspath("certnew.pem"), "w+")
fp_cert.write(str(HTTPS_SECRETS['clientcert']))
fp_cert.close()

fp_key = open(os.path.abspath("keynew.pem"), "w+")
fp_key.write(str(HTTPS_SECRETS['clientprivate']))
fp_key.close()

kv = nkvClient(zmq_end_point, False)
kv.write("newkey","test1",'{"name":"testuser", "age":37}', contentFormat="JSON")
response = kv.read('newkey', 'test1', contentFormat="JSON")
print("response received " + str(response))

ts = ntsClient(zmq_end_point, False)
ts.write("newkeyts", '{"name":"testuserts", "age":37}', contentFormat="JSON")
response = ts.latest("newkeyts",  contentFormat="JSON")
print("response received " + str(response))
del kv

app = Flask(__name__)

@app.route("/ui")

def hello():
    return "Hello World!"

if __name__ == "__main__":
     print("Nothing")
     ctx = ('certnew.pem', 'keynew.pem')
     app.run(host='0.0.0.0', port=8080, ssl_context=ctx)
