# databox-hello-world-driver
A simple python hello-world-driver which connects with Databox.
<<<<<<< HEAD

The databox container manager install a driver, it reads the SLA associated with the driver and set following Environment Variables:

DATABOX_ARBITER_ENDPOINT
DATABOX_LOCAL_NAME
DATABOX_STORE_ENDPOINT
DATABOX_ROOT_CA
Localcontainername_PEM
Localcontainername.pem
Localcontainername_key=ARBITER_TOKEN

2. Fetch data from outside and store in the datastore.
3. First to write data, it checks Arbiter for all datastores.
4. Then it writes to the datastore by composing a request - it sends arbiter key in the request.

when a datastore gets a request from a driver to read/write - (what does it do?)


index.js fetches manifest from appstore ->  main.js - > server.js -> container-manager.js

/api/datasource/list
/api/installed/list
/api/:type/list
/list-apps
/api/install

=======
>>>>>>> 53691a3e4d188d1a7be4876005f67e540e368b86
