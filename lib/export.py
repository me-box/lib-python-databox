import lib.utils as utils
import os
import json

try:
    if "DATABOX_EXPORT_SERVICE_ENDPOINT" in os.environ:
        exportServiceURL = os.environ['DATABOX_EXPORT_SERVICE_ENDPOINT']
except NameError:
        print("Export service endpoint is not defined")
        exportServiceURL=''

def longpoll(destination, payload):
    newurl = exportServiceURL + '/lp/export'
    return utils.makeStoreRequest(method = 'POST', jsonData = {'id': '', 'uri': destination, 'data': json.dump(payload)}, url=newurl)

def queue(href, key, data):
    raise NotImplementedError