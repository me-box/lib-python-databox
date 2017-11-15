import lib.utils as utils
import websocket
import urllib3
from pyee import EventEmitter
import json
import ssl
CM_HTTPS_CA_ROOT_CERT = open("/run/secrets/DATABOX_ROOT_CA").read()

ee = EventEmitter()

storeUrl=''
if CM_HTTPS_CA_ROOT_CERT is not None:
    http = urllib3.PoolManager(
    ca_certs='/run/secrets/DATABOX_ROOT_CA')
else:
    print('Warning: No HTTPS root certificate provided so Databox HTTPS certificates will not be checked')

def on_message(ws, message, data):
    jsonData = json.dump(data)
    ee.emit('data',  storeUrl.host, data.datasource_id, data.data)
    print(message)

def on_error(ws, error):
    #ee.emit('error')
    print(error)

def on_close(ws):
    ee.emit('close')
    print("### closed ###")

def on_open(ws):
    print("Websocket Open")

def connect(href):
        storeURL = urllib3.util.parse_url(href)
        storeUrl = storeURL
        websocket.enableTrace(True)
        token = utils.requestToken(storeURL.host, '/ws', 'GET')
        print("token received " + str(token))

        try:
            ws = websocket.WebSocketApp('wss://' + storeURL.host + ':' + str(storeURL.port) + '/ws', headers={'x-api-key': str(token)}, on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
            ws.on_open = on_open
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except Exception as e:
            print(e)
            print("[Websocket Connection Error]")


def subscribe(href, dataSourceID, type1):
        if(type1 is None or not type1):
            type1 = dataSourceID
            dURL = urllib3.util.parse_url(href)
            href = dURL.scheme + ':' + '//' + dURL.host
            dataSourceID = dURL.path.replace('/', '')
        return utils.makeStoreRequest(method='GET', jsonData={'True': True}, url=href + '/sub/' + dataSourceID + '/' + type1)

def unsubscribe(href, dataSourceID, type):
        if (type1 is None or not type1):
            type1 = dataSourceID
            dURL = urllib3.util.parse_url(href)
            href = dURL.scheme + ':' + '//' + dURL.host
            dataSourceID = dURL.path.replace('/', '')
        return utils.makeStoreRequest(method='GET', jsonData={'True': True}, url=href + '/sub/' + dataSourceID + '/' + type1)

