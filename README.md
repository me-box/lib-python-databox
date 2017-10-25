# python-databox-library

This repo includes python driver and app templates with databox-python library with basic APIs.  Copy lib folder in your application directory and import lib in your driver/app python file.
```
import lib as databox
```
Databox python library provides following funtions:

```
databox.waitForStoreStatus(href, status, maxRetries)
databox.makeStoreRequest(method, jsonData, url)
databox.makeArbiterRequest(method, path, data)
databox.requestToken(hostname, endpoint, method)
databox.getRootCatalog()
databox.listAvailableStores()
databox.registerDatasource(href, metadata)
databox.export.longpoll(destination, payload)
databox.key_value.read(href, key)
databox.key_value.write(href, key, data)
```

The usecases of these functions are in [Driver](./samples/driver-hello-world/test.py) and [App](./samples/app-hello-world/test.py)
