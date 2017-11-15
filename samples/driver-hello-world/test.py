__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

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
#print(dpem)
HTTPS_SECRETS = json.loads(dpem)

fp_cert = open(os.path.abspath("certnew.pem"), "w+")
fp_cert.write(str(HTTPS_SECRETS['clientcert']))
fp_cert.close()


fp_key = open(os.path.abspath("keynew.pem"), "w+")
fp_key.write(str(HTTPS_SECRETS['clientprivate']))
fp_key.close()

data = {}
#Check if the store is ready for reading or writing
dx = databox.waitForStoreStatus(store, 'active', 100)
print("Store is active now")


#write key-value pair in the store
res= databox.key_value.write(store, 'test', { 'foo': 'bar' })
print("response "+str(res))

#Get the root catalog of all stores from the arbiter
cat = databox.getRootCatalog()
print("Root Catalog " + str(cat))

#Register a datastore catalog with the store.
dataSourceTemp = json.dumps({
        "description":'helloworld',
        "contentType":'text/json',
        "vendor":'Databox Inc.',
        "type":'helloworld',
        "datasourceid":'helloworld',
        "storeType":'store-json'
        })
response = databox.registerDatasource(store,dataSourceTemp)
print("Response from the data registered " + str(response))

dataSourceTempOaas= json.dumps({
        "description": 'oaas ',
        "contentType": 'text/json',
        "vendor": 'Databox Inc.',
        "type": 'oaasunknown',
        "datasourceid": 'oaasunknown',
        "storeType": 'store-json'
})

response = databox.registerDatasource(store,dataSourceTempOaas)
res = databox.time_series.write(store, 'oaasunknown', 1)
print("response from time series "+str(res))
datareceived = databox.time_series.latest(store,'oaasunknown')
print("Recent Data received " + str(datareceived))
datareceived = databox.time_series.range(store,'oaasunknown', 1, 2)
print("Data received " + str(datareceived))
#databox.subscriptions.connect(store)


