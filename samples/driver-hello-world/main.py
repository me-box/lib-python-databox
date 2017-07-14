__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

import lib.utils as databox
import urllib3
import os
import json
from OpenSSL import SSL
from flask import Flask


store= os.environ['DATABOX_STORE_ENDPOINT']
print('Store' + store)

dpem = os.O_RDONLY("/run/secrets/DATABOX_PEM")
HTTPS_SECRETS = json.load(dpem.read())
dpem.close()

credentials = {
  "key":  HTTPS_SECRETS.clientprivate or '',
  "cert": HTTPS_SECRETS.clientcert or '',
}

databox.waitForStoreStatus(store,'active',100)
cert = ''
key = ''
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(ssl_context= (credentials["cert"], "key"))