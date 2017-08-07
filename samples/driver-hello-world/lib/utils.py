import urllib3
import os
import json
import base64
import certifi
from urllib.parse import urlencode
import time


arbiter = os.environ['DATABOX_ARBITER_ENDPOINT']
hostname = os.environ['DATABOX_LOCAL_NAME']

arbiterToken = open("/run/secrets/ARBITER_TOKEN", "rb").read()
arbiterTokenbase64 = base64.b64encode(arbiterToken)

CM_HTTPS_CA_ROOT_CERT = open("/run/secrets/DATABOX_ROOT_CA").read()

if CM_HTTPS_CA_ROOT_CERT is not None:
    http = urllib3.PoolManager(
    ca_certs='/run/secrets/DATABOX_ROOT_CA')
else:
    print('Warning: No HTTPS root certficate provided so Databox HTTPS certificates will not be checked')

#def getHttpsCredentials():
#    credentials = {}
#    try:
#        credentials = {"key": open("/run/secrets/DATABOX.pem").read() or '', "cert": open("/run/secrets/DATABOX.pem").read() or ''}
#    except:
#        print("Warning: No HTTPS certficate not provided HTTPS certificates missing.")
#        credentials = {}
#    return credentials


def makeArbiterRequest(method, path, data):
    try:
        target_s = data['target']
        path_s = data['path']
        method_s = data['method']
        url = arbiter + path
        encoded1 = {'target': target_s, 'path':  path_s, 'method': method_s}
        encoded_body = json.dumps(encoded1)
        response = http.request(method=method, url=url, body=encoded_body, headers={'X-Api-Key': arbiterTokenbase64, 'Content-Type':'application/json'})
        if(response.status < 200 and response.status >= 300 ):
            raise Exception("[AP1 Error]" + str(response.status))
        else:
            return response.data
    except Exception as err:
        print("[makeArbiterRequest] error" + repr(err))

def requestToken(hostname, endpoint, method):
    return makeArbiterRequest('POST', '/token', {
		'target': hostname,
		'path':   endpoint,
		'method': method
	})

def makeStoreRequest(method, url):
    tokenCache = {}
    route = {'target': urllib3.util.parse_url(url).host, 'path': urllib3.util.parse_url(url).path, 'method': 'GET'}
    routeHash = json.dumps(route)
    if(routeHash not in tokenCache):
        response = requestToken(route['target'], route['path'], route['method'])
        if(response is not None):
            coded64response = base64.b64encode(response)
            tokenCache[routeHash] = coded64response
            try:
                response1 = http.request(method=method, url=url, headers={'X-Api-Key': tokenCache[routeHash]})
                return response1
            except Exception as err:
                print("[makeStoreRequest] error" + repr(err))
        else:
            return response
    else:
        try:
            response1 = http.request(method=method, url=url, headers={'X-Api-Key': tokenCache[routeHash]})
            return response1
        except Exception as err:
            print("[makeStoreRequest] error" + repr(err))

def waitForStoreStatus(href, status, maxRetries):
    try:
        tries = 1
        rurl = urllib3.util.parse_url(href)
        newurl = rurl.scheme + ':'+'//' + rurl.host +':'+ str(rurl.port) + '/status'
        statusreceived = makeStoreRequest(method = 'GET', url=newurl)
        while((statusreceived is None) and (tries < maxRetries)):
          tries = tries + 1
          print("[waitForStoreStatus] Retrying in 2s...")
          time.sleep(2)
          statusreceived = makeStoreRequest(method='GET', url=newurl)

        if(str(statusreceived.data,'utf8') == str(status)):
            return
        else:
            raise Exception("[AP1 Error]" + str(statusreceived.status))
    except Exception as err:
        print(err)
