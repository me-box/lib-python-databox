import lib.utils as utils


def read(href, key):
    print("read called")
    newurl= href +'/' + key +'/kv'
    return utils.makeStoreRequest(method='GET', jsonData={'True': True}, url=newurl)

def write(href, key, data):
    print("write called")
    if(data):
        newurl = href + '/' + key + '/kv'
    else:
        newurl = href
        data = key
    return utils.makeStoreRequest(method='POST', jsonData=data, url=newurl)

