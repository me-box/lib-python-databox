import urllib3
import os
import requests
import json
import base64


arbiterURL = os.environ['DATABOX_ARBITER_ENDPOINT']
hostname = os.environ['DATABOX_LOCAL_NAME']
print("ArbiterURL "+arbiterURL)
print("Hostname "+hostname)

arbiterToken = open("/run/secrets/ARBITER_TOKEN",  "rb").read()
print(arbiterToken)

CM_HTTPS_CA_ROOT_CERT = open("/run/secrets/DATABOX_ROOT_CA").read()



if CM_HTTPS_CA_ROOT_CERT is not None:
    http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=CM_HTTPS_CA_ROOT_CERT)
else:
    print('Warning: No HTTPS root certficate provided so Databox HTTPS certificates will not be checked')


def makeArbiterRequest(method, path, json):
    print("Inside Arbiter Request")
    http.request(method=method, url=arbiterURL + path, json=json, headers={ 'X-Api-Key': arbiterToken }, )

def requestToken(hostname, endpoint, method):
    print("Request Token")
    return makeArbiterRequest('POST', '/token', {
		'target': hostname,
		'path':   endpoint,
		'method': method
	})

def makeStoreRequest(method, url):
    tokenCache = {}
    print(method)
    print(url)
    route = { 'target': urllib3.util.parse_url(url).host,  'path': urllib3.util.parse_url(url).path, 'method': 'GET'}
    routeHash = json.dumps(route);
    if (routeHash not in tokenCache):
        token = requestToken(route['target'], route['path'], route['method'])
        tokenCache[routeHash] = token
        return token
    else:
        return tokenCache[routeHash]


def waitForStoreStatus(href, status, maxRetries):
    try:
        rurl = urllib3.util.parse_url(href)
        newurl = rurl.scheme + '//' + rurl.host + '/status'
        statusreceived = makeStoreRequest(method = 'GET', url=newurl)
        while(statusreceived != status):
            statusreceived = makeStoreRequest(method='GET', url=newurl)
            print("Retrying -Current status is " + statusreceived)
    except Exception as err:
        print(err)
