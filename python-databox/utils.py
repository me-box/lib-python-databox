import urllib3
import os
import requests
import json
from retrying import retry


arbiterURL = os.environ['DATABOX_ARBITER_ENDPOINT']
hostname = os.environ['DATABOX_LOCAL_NAME']
print("ArbiterURL"+arbiterURL)
print("Hostname"+hostname)

fd= os.O_RDONLY("/run/secrets/ARBITER_TOKEN")
arbiterToken = fd.read()
fd.close()

fa = os.O_RDONLY("/run/secrets/DATABOX_ROOT_CA")
CM_HTTPS_CA_ROOT_CERT = fa.read()
fa.close()


if (CM_HTTPS_CA_ROOT_CERT):
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
		target: hostname,
		path:   endpoint,
		method: method
	})

def makeStoreRequest(method, url):
    print(method)
    print(url)
    route = { 'target': urllib3.util.parse_url(url).host,  'path': urllib3.util.parse_url(url).path, }



def waitForStoreStatus(href, status, maxRetries):
    try:
        rurl = urllib3.util.parse_url(href)
        newurl = rurl.scheme + '//' + rurl.host + '/status'
        makeStoreRequest(method = 'GET', url=newurl)
    except Exception as err:
        print(err)

waitForStoreStatus('http://google.com/mail/', 'none', 2   )
