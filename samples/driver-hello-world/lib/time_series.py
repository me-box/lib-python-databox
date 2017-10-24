import lib.utils as utils

def latest(href, dataSourceID):
        href += '/' + dataSourceID
        utils.makeStoreRequest(method='GET',json={"True":True}, url= href +'/ts/latest')

def since(href, dataSourceID, startTimestamp):
        if startTimestamp:
            href += '/' + dataSourceID
        else:
            startTimestamp = dataSourceID
        utils.makeStoreRequest(method='GET', json={startTimestamp}, url=href + '/ts/since')

def range(href, dataSourceID, startTimestamp, endTimestamp):
        if endTimestamp:
            href += '/' + dataSourceID
        else:
            endTimestamp = startTimestamp
            startTimestamp = dataSourceID
        utils.makeStoreRequest(method='GET', json={startTimestamp,endTimestamp}, url=href + '/ts/range')

def write(href, dataSourceID, data):
        if data:
            href += '/' + dataSourceID
        else:
            data = dataSourceID
        utils.makeStoreRequest(method='POST', json={data: data}, url=href + '/ts')










