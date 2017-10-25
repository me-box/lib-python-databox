# databox app-hello-world
A simple python app-hello-world which runs in the  Databox.

When an app is installed from the Databox UI, this passes the request to  the databox container manager (CM), which installs the app. CM reads the SLA associated with the app and set the Environment Variables: The environment variables that can be accessed inside the databox app can be listed by:
```
import os
import lib as databox

for a in os.environ: 
print( a, '=', os.getenv(a))
```
This will show following variables for a Databox App:
```
DATABOX_ARBITER_ENDPOINT = https://arbiter:8080
DATABOX_LOCAL_NAME = app-hello-world
DATABOX_STORE_ENDPOINT = https://app-hello-world-store-json:8080
Localcontainername_key=ARBITER_TOKEN
DATABOX_EXPORT_SERVICE_ENDPOINT = https://export-service:8080
DATASOURCE_DS_helloworld = {"item-metadata":[{"val":"hello-world","rel":"urn:X-hypercat:rels:hasDescription:en"},

{"val":"text/json","rel":"urn:X-hypercat:rels:isContentType"},{"val":"Databox Inc.","rel":"urn:X-databox:rels:hasVendor"},

{"val":"helloworld","rel":"urn:X-databox:rels:hasType"},{"val":"helloworld","rel":"urn:X-databox:rels:hasDatasourceid"},

{"val":"store-json","rel":"urn:X-databox:rels:hasStoreType"}],"href":"https://driver-hello-world-store-json:8080/helloworld"}
```
From DATASOURCE_DS_helloworld, we can extract endpoints of the driver store. In this example, it is
```
driverStore = "https://driver-hello-world-store-json:8080"
```

Therefore, 
1. to integrate an app as a databox app, the app needs to have access to the keys and token to access stores.
2. App requests access to a data-store by configuring it in the databox-manifest.json file - template shown below. When container manager install the app, it also launches a data-store of the requested type.
3. In a "store" of type "store-json", following function permissions are

```
method: GET, endpoint:  app-hello-world-store-json/cat (From container-manager)
method: GET, endpoint:  app-hello-world-store-json/status (from the app)
method: GET, endpoint:  app-hello-world-store-json/ws (from the app)
method: GET, endpoint:  app-hello-world-store-json/sub/* (from the app)
method: GET, endpoint:  app-hello-world-store-json/unsub/* (from the app)
method: POST, endpoint: app-hello-world-store-json/cat (from the app)

```
4. Configure and create local data store stream - template of information which need to provide to the API.
```
 template = {	description: 'App Description',
        	contentType: 'text/json',
        	vendor: 'Databox Inc.',
        	type: 'appHelloworldstream',
       		datasourceid: 'appHelloworldstream',
       	 	storeType: 'store-json'
	   }
localStore= os.environ['DATABOX_STORE_ENDPOINT']	   
	   
databox.registerDatasource(localStore, template)
```
5. Write and Read data to local datastore stream.
```
databox.key_value.write(localStore, 'appHelloworldstream', { 'foo': 'bar' })
```
response = databox.key_value.read(localStore, 'appHelloworldstream')

6.  Read from driver store.

res = databox.key_value.read(driverStore, 'appHelloworldstream')

7. Export data to an allowed external endpoint.
databox.export.longpoll('https://export.amar.io/', {"appHelloworldstream": res.decode('utf8').replace("'", '"')})


### Manifest template 
In the manifest, two important things to notice here are "databox-type" and "resource-requirements" - "store". When the driver is installed, a data store of type mentioned in "store" is launched.

```
{	"manifest-version": 1,
	"name": "app-hello-world",
	"databox-type": "app",
	"version": "0.1.0",
	"description": "A template Databox app in Python",
	"author": "Poonam Yadav <p.yadav@acm.org> (http://poonamyadav.net/)",
	"license": "MIT",
	"tags": [
		"template",
		"app",
		"mock",
		"python"
	],

	"homepage": "https://github.com/me-box/lib-python-databox",
	"repository": {
		"type": "git",
		"url": "git+https://github.com/me-box/lib-python-databox"
	},
	
	"allowed-combinations": [],
   	
	"packages": [
		{
			"name": "Hello World ",
			"purpose": "Hello - world assumption",
			"install": "required",
			"risks": "Leaking all your data.",
			"benefits": "Demo of the Databox apps.",
			"datastores": ["DS_helloworld"] 
		}
	],
	"datasources": [
		{
			"type": "helloworld",
			"required": true,
			"name": "helloworld",
			"clientid": "DS_helloworld",
			"granularities": []
		}
	],

	"export-whitelist": [
		{
			"url": "https://export.amar.io/",
			"description": "Databox export destination request logger"
		}, {
			"url": "https://wtfismyip.com/json",
			"description": "Your public IP, location, hostname, ISP, and Tor status"
		}
	],
	
	"resource-requirements": {
		"store": "store-json"
	}
}


