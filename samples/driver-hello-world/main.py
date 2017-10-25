__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

import lib as databox
import urllib3
import os
import json
from flask import Flask
import ssl

store= os.environ['DATABOX_STORE_ENDPOINT']
print('Store ' + store)

hostname = os.environ['DATABOX_LOCAL_NAME']

dpem = open("/run/secrets/DATABOX_PEM").read()

HTTPS_SECRETS = json.loads(dpem)

fp_cert = open(os.path.abspath("certnew.pem"), "w+")
fp_cert.write(str(HTTPS_SECRETS['clientcert']))
fp_cert.close()

fp_key = open(os.path.abspath("keynew.pem"), "w+")
fp_key.write(str(HTTPS_SECRETS['clientprivate']))
fp_key.close()

data = {}

dx = databox.waitForStoreStatus(store, 'active', 100)
print("Store is active now")
cat = databox.getRootCatalog()
print("Root Catalog " + str(cat))

dataSourceTemp = json.dumps({
    "description": 'helloworld',
    "contentType": 'text/json',
    "vendor": 'Databox Inc.',
    "type": 'helloworld',
    "datasourceid": 'helloworld',
    "storeType": 'store-json'
})
response = databox.registerDatasource(store,dataSourceTemp)

app = Flask(__name__)

@app.route("/ui")
def hello():
    return "Hello World!"

if __name__ == "__main__":
     print("Nothing")
     ctx = ('certnew.pem', 'keynew.pem')
     app.run(host='0.0.0.0', port=8080, ssl_context=ctx)
