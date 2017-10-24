import lib.utils as utils
import os
import json

try:
    DATABOX_EXPORT_SERVICE_ENDPOINT
    exportServiceURL = os.environ['DATABOX_EXPORT_SERVICE_ENDPOINT']
except NameError:
        print("Export service endpoint is not defined")
        exportServiceURL=''

def longpoll(destination, payload):
    #raise NotImplementedError
    newurl = exportServiceURL + '/lp/export'
    return utils.makeStoreRequest(method = 'POST', jsonData = {'id': '', 'uri': destination, 'data': json.dump(payload)}, url=newurl)

def queue(href, key, data):
    raise NotImplementedError