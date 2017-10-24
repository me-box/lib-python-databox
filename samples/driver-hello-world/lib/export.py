import lib.utils as utils
import os
import json

#exportServiceURL = os.environ['DATABOX_EXPORT_SERVICE_ENDPOINT']

def longpoll(destination, payload):
    raise NotImplementedError
    #newurl = exportServiceURL + '/lp/export'
    #return utils.makeStoreRequest(method = 'POST', json = {id: '', uri: destination, data: json.dump(payload)}, url=newurl)

def queue(href, key, data):
    raise NotImplementedError