__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

import lib.utils as databox
import urllib3
import os
import json
from flask import Flask
import ssl

store= os.environ['DATABOX_STORE_ENDPOINT']
print('Store' + store)

dpem = open("/run/secrets/DATABOX_PEM").read()
HTTPS_SECRETS = json.loads(dpem)
print (dpem)

fp_cert =  open(os.path.abspath('certs.crt'), 'w+')
fp_cert.write(HTTPS_SECRETS['clientcert'] or '')

fp_key = open(os.path.abspath('keys.key'), 'w+')
fp_key.write(HTTPS_SECRETS['clientprivate'] or '')
ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

context = (os.path.abspath('certs.crt'), os.path.abspath('keys.key'))
print(context)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8080, ssl_context= context)
