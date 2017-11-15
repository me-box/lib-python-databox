import lib.utils as utils

def latest(href, dataSourceID):
        href += '/' + dataSourceID
        return utils.makeStoreRequest(method='GET',jsonData={"True":True}, url= href +'/ts/latest')

def since(href, dataSourceID, startTimestamp):
        if startTimestamp:
            href += '/' + dataSourceID
        else:
            startTimestamp = dataSourceID
        return utils.makeStoreRequest(method='GET', jsonData={"startTimestamp":startTimestamp}, url=href + '/ts/since')

def range(href, dataSourceID, startTimestamp, endTimestamp):
        if endTimestamp:
            href += '/' + dataSourceID
        else:
            endTimestamp = startTimestamp
            startTimestamp = dataSourceID
        return utils.makeStoreRequest(method='GET', jsonData={"startTimestamp":startTimestamp,"endTimestamp":endTimestamp}, url=href + '/ts/range')

def write(href, dataSourceID, data):
        if data:
            href += '/' + dataSourceID
        else:
            data = dataSourceID
        return utils.makeStoreRequest(method='POST', jsonData={'data': data}, url=href + '/ts')










