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
try:
        driverStore = json.loads(os.environ['DATASOURCE_DS_helloworld'])
        driverStore_endPoint = driverStore["href"]
        print('driverStore ' + str(driverStore_endPoint))
        rurl = urllib3.util.parse_url(driverStore_endPoint)
        ds_url = rurl.scheme + ':' + '//' + rurl.host + ':' + str(rurl.port)
        print('driverStore URL ' + str(ds_url))
except NameError:
        print("error")
        driverStore_endPoint = '{}'

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
print("response write"+str(res))

response = databox.key_value.read(store, 'test')
print("response received"+str(response))

#Get the root catalog of all stores from the arbiter
cat = databox.getRootCatalog()
print("Root Catalog " + str(cat))

list= databox.listAvailableStores()
print("available stores")
print(list)

#Register a datastore "stream/key" with the local store catalog.
dataSourceTemp = json.dumps({
        "description":'hello-world',
        "contentType":'text/json',
        "vendor":'Databox Inc.',
        "type":'helloworld',
        "datasourceid":'helloworld',
        "storeType":'store-json'
        })
response = databox.registerDatasource(store,dataSourceTemp)
print("Response from the data registered " + str(response))

#read from the driver data stream "helloworld"
response = databox.key_value.read(ds_url, 'helloworld')
print("response received from driver store"+str(response))

#export data to external url 
databox.export.longpoll('https://export.amar.io/', {"helloworld": response.decode('utf8').replace("'", '"')})

#Check all environment variables
for a in os.environ:
    print('Var: ', a, 'Value: ', os.getenv(a))