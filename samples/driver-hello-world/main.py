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
print('Store ' + store)

pem = databox.getHttpsCredentials()

app = Flask(__name__)

@app.route("/ui")
def hello():
    return "Hello World!"

if __name__ == "__main__":
     print("Nothing")
     ctx = (pem, pem)
     app.run(host='0.0.0.0', port=8080, ssl_context=ctx)
