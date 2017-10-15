import utils


def read(href, key):
    print("read called")
    newurl= href +'/' + key +'/kv'
    return utils.makeStoreRequest(method='GET', json=true, url=newurl)


def write(href, key, data):
    print("write called")
    newurl = href + '/' + key + '/kv'
    return utils.makeStoreRequest(method='POST', json=data, url=newurl)

