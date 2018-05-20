# python-databox-library

This repo includes python driver and app templates with databox-python library with basic APIs.  Copy lib folder in your application directory and import lib in your driver/app python file.
```
import lib as databox
from databox.core_store import NewKeyValueClient as nkvClient
from databox.core_store import NewTimeSeriesClient as ntsClient
```
Databox python library provides following funtions:

## Key/Value API

### Write entry

URL: /kv/<id>/<key>
Method: POST
Parameters: JSON body of data, replace <id> and <key> with a string
Notes: store data using given key
```
nkvClient.write(id, key, payload, contentFormat)
```

### Read entry

URL: /kv/<id>/<key>
Method: GET
Parameters: replace <id> and <key> with a string
Notes: return data for given id and key 
```
nkvClient.read(id, key, contentFormat)
```

## Time series API


### Write entry (auto-generated time)
URL: /ts/<id>
Method: POST
Parameters: JSON body of data, replace <id> with a string
Notes: add data to time series with given identifier (a timestamp will be calculated at time of insertion)
```
ntsClient.write(id, payload, contentFormat)
```

### Write entry (user-specified time)

### Read latest entry
URL: /ts/<id>/latest
Method: GET
Parameters: replace <id> with an identifier
Notes: return the latest entry
```
ntsClient.latest(id, contentFormat)
```
### Read last number of entries

### Read earliest entry

### Read first number of entries

### Read all entries since a time (inclusive)

### Read all entries in a time range (inclusive)

### Delete all entries since a time (inclusive)

### Delete all entries in a time range (inclusive)

### Length of time series

The usecases of these functions for the test purpose included in  the Sample [Driver](./samples/driver-hello-world/test.py) and the sample [App](./samples/app-hello-world/test.py).
