import urllib3
import os
import json
import base64
from urllib.parse import urlencode
import time
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'../' '.env')
load_dotenv(dotenv_path)
print(dotenv_path)
print("Testing")



arbiter = os.environ['DATABOX_ARBITER_ENDPOINT']
hostname = os.environ['DATABOX_LOCAL_NAME']
CORE_STORE_KEY = "vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<"
if os.path.isfile('/run/secrets/ZMQ_PUBLIC_KEY'):
    with open('/run/secrets/ZMQ_PUBLIC_KEY') as f:
        CORE_STORE_KEY = f.read()
    f.close()
else:
    print("'Warning: No ZMQ_PUBLIC_KEY provided so Databox will use the default key")

arbiterToken = ""
if(os.path.exists("/run/secrets/ARBITER_TOKEN")):
    arbiterToken = open("/run/secrets/ARBITER_TOKEN", "rb").read()
    arbiterTokenbase64 = base64.b64encode(arbiterToken)
elif (os.path.exists("/run/secrets/CM_KEY")):
    arbiterToken = open("/run/secrets/CM_KEY", "rb").read()
    arbiterTokenbase64 = base64.b64encode(arbiterToken)
else:
    print('Warning: No ARBITER_TOKEN provided so Databox will not request tokens from the arbiter')


CCM_HTTPS_CA_ROOT_CERT = None
try:
    CM_HTTPS_CA_ROOT_CERT = open("/run/secrets/DATABOX_ROOT_CA").read()
except OSError:
    CM_HTTPS_CA_ROOT_CERT = None
else:
    if CM_HTTPS_CA_ROOT_CERT is not None:
        https = urllib3.PoolManager(ca_cer='/run/secrets/DATABOX_ROOT_CA')
    else:
        print('Warning: No HTTPS root certificate provided so Databox HTTPS certificates will not be checked')
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
        url = arbiter + path
        print(data)
        encoded_body = json.dumps(data)
        print(encoded_body)
        response = http.request(method=method, url=url, body=encoded_body, headers={'X-Api-Key': arbiterTokenbase64, 'Content-Type': 'application/json'})
        if (response.status < 200 and response.status >= 300):
            raise Exception("[API Error]" + str(response.status))
        else:
            print("Response from arbiter " + str(response.data))
            return response.data
    except Exception as err:
        print("[makeArbiterRequest] error " + repr(err))


def requestToken(hostname, endpoint, method):
    print('hostname ' + hostname)
    token = makeArbiterRequest('POST', '/token', { 'target': hostname, 'path':   endpoint,'method': method })
    print(token)
        #if (token is not None):
        #    tokenCache[routeHash] = token
        # else:
        #    print("Error in getting token from arbiter")
    #else:
       # token = tokenCache[routeHash]

    return token


def makeStoreRequest(method, jsonData, url):
    tokenCache = {}
    encoded_body = json.dumps(jsonData)
    route = {'target': urllib3.util.parse_url(url).host, 'path': urllib3.util.parse_url(url).path, 'method': method}
    routeHash = json.dumps(route)
    if (routeHash not in tokenCache):
        token = requestToken(route['target'], route['path'], route['method'])
        if (token is not None):
            #coded64token = base64.b64encode(token)
            #tokenCache[routeHash] = coded64token
            tokenCache[routeHash] = token
            try:
                store_response = http.request(method=method, url=url, body=encoded_body, headers={'X-Api-Key': tokenCache[routeHash], 'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json'})
                return store_response.data
            except Exception as err:
                print("[makeStoreRequest] error" + repr(err))
        else:
            print("No token received from arbiter..so retry again")
            return token
    else:
        try:
            store_response = http.request(method=method, url=url, body=encoded_body, headers={'X-Api-Key': tokenCache[routeHash], 'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json'})
            return store_response.data
        except Exception as err:
            print("[makeStoreRequest] error" + repr(err))


def waitForStoreStatus(href, status, maxRetries):
    try:
        tries = 1
        rurl = urllib3.util.parse_url(href)
        newurl = rurl.scheme + ':' + '//' + rurl.host + ':' + str(rurl.port) + '/status'
        statusreceived = makeStoreRequest(method='GET', jsonData={'True': True}, url=newurl)
        while ((statusreceived is None) and (tries < maxRetries)):
            tries = tries + 1
            print("[waitForStoreStatus] Retrying in 2s...")
            time.sleep(2)
            statusreceived = makeStoreRequest(method='GET', jsonData={'True': True}, url=newurl)
            print("status recieved " + statusreceived)
            if (str(statusreceived, 'utf8') == str(status)):
                return
            else:
                raise Exception("[AP1 Error]" + str(statusreceived.status))
    except Exception as err:
        print(err)