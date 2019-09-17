__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

import pythonzestclient as zestClient
import lib.config as config
import lib.arbiter_client as arbiterClient
import urllib3
import os
import json
from flask import Flask
import ssl
from io import StringIO
import base64


# StoreClient returns a new client to read and write data to stores
# storeEndpoint is provided in the DATABOX_ZMQ_ENDPOINT environment variable
# and arbiterEndpoint is provided by the DATABOX_ARBITER_ENDPOINT environment variable
#to databox apps and drivers.

class coreStoreClient:
    def __init__(self, config, zestEndpoint, zestDealerEndpoint,  zestCli, arbiterCli):
        self.config = config
        self.zestEndpoint = zestEndpoint
        self.zestDealerEndpoint = zestDealerEndpoint
        self.zestCli = zestCli
        self.arbiterCli = arbiterCli

    def newStoreClient(config, zestEndpoint, zestDealerEndpoint,  zestCli, arbiterCli):
        return coreStoreClient(config, zestEndpoint, zestDealerEndpoint,  zestCli, arbiterCli)

    def RegisterDatasource(self, DataSourceMetadata):
        return _registerDatasource(self.arbiterCli, self.zestCli, DataSourceMetadata)

    def GetDatasourceCatalogue(self):
        return _read(self.arbiterCli, self.zestCli, '/cat', '/cat', 'JSON')

    def getStoreUrlFromHypercat(self, hypercat):
        dsm = HypercatToSourceDataMetadata(hypercat)
        u =  urllib3.util.parse_url(hypercatObj.href)
        return u.scheme + '//' + u.host


    def read(self, dataSourceID, key, contentFormat = 'JSON'):
        path = "/kv/" + dataSourceID + "/" + key
        return _read(self.arbiterCli, self.zestCli, path, path, contentFormat)

    def write(self, dataSourceID, key, payload, contentFormat = 'JSON'):
        print("Inside write")
        path = "/kv/" + dataSourceID + "/" + key
        return _write(self.arbiterCli, self.zestCli, path, path, payload, contentFormat)

        #def __del__(self):
        #   self.store.closeSockets()


def _registerDatasource(arbiterClient, zestClient, DataSourceMetadata):
    if ValidateDataSourceMetadata(DataSourceMetadata) == True:
        try:
            hyperCatObj = DataSourceMetadataToHypercat(zestClient.endpoint + '/' + DataSourceMetadata.StoreType + '/', DataSourceMetadata)
            hyperCatString = json.dumps(hyperCatObj)
            _write(arbiterClient, zestClient, '/cat', '/cat', hyperCatString, 'JSON')
        except ValueError:
            print("RegisterDatasource Error "+ ValueError)
    else:
        print("InValid DataSourceMetaData ")

def DataSourceMetadataToHypercat(endpoint, metadata):
    ValidateDataSourceMetadata(metadata)
    cat = {'item-metadata': [{"rel": "urn:X-hypercat:rels:hasDescription:en",
                              "val": metadata['Description']},
                             {"rel": "urn:X-hypercat:rels:isContentType",
                              "val": metadata['ContentType']},
                             {"rel": "urn:X-databox:rels:hasVendor",
                              "val": metadata['Vendor']},
                             {"rel": "urn:X-databox:rels:hasType",
                              "val": metadata['DataSourceType']},
                             {"rel": "urn:X-databox:rels:hasDatasourceid",
                              "val": metadata['DataSourceID']},
                             {"rel": "urn:X-databox:rels:hasStoreType",
                              "val": metadata['StoreType']}],
           'href': endpoint + metadata['DataSourceID']

           }

    if(metadata.IsActuator):
        cat['item-metadata'].push({"rel":"urn:X-databox:rels:isActuator", "val":metadata.IsActuator})

    if(metadata.Unit):
        cat['item-metadata'].push({"rel":"urn:X-databox:rels:hasUnit","val":metadata.Unit})

    if (metadata.Location):
        cat['item-metadata'].push({"rel":"urn:X-databox:rels:hasLocation","val":metadata.Location})

    return cat




def ValidateDataSourceMetadata(DataSourceMetadata):
    try:
        if not DataSourceMetadata or type(DataSourceMetadata) !='object' or not DataSourceMetadata.Description or not DataSourceMetadata.ContentType or not DataSourceMetadata.Vendor or not DataSourceMetadata.DataSourceType or not DataSourceMetadata.DataSourceID or not DataSourceMetadata.StoreType:
            raise ValueError
        else:
            checkStoreType(DataSourceMetadata.StoreType)
    except ValueError:
        print("Error:: Not a valid DataSourceMetadata object missing required property")
        return False

    return True

def checkStoreType(StoreType):
    try:
        switcher = {"kv": True, "ts": True, "ts/blob": True}
        if switcher.get(StoreType) == True:
            return True
        else:
            raise ValueError
    except ValueError:
        print("Error:: DataSourceMetadata invalid StoreType can be kv,ts or ts/blob")



class StoreClient:
    def __init__(self, storeEndpoint, arbiterEndpoint, enableLogging):
        self.zestEndpoint = storeEndpoint
        self.zestDealerEndpoint = storeEndpoint.replace(":5555", ":5556")
        print(config.CORE_STORE_KEY)
        self.zestCli = zestClient.PyZestClient(config.CORE_STORE_KEY, self.zestEndpoint,self.zestDealerEndpoint,  enableLogging)
        print(self.zestCli)
        #arbiterCli = arbiterClient(arbiterEndpoint, enableLogging)
        self.arbiterCli = arbiterClient.new_arbiter_client(arbiterEndpoint, enableLogging)
        self.storeCli = coreStoreClient.newStoreClient(config, self.zestEndpoint, self.zestDealerEndpoint,  self.zestCli, self.arbiterCli)
        print("client " + str(self.storeCli) )

    def NewStoreClient(storeEndpoint, arbiterEndpoint, enableLogging):
        return StoreClient(storeEndpoint, arbiterEndpoint, enableLogging)



def _read(arbiterClient, zestClient, path, tokenPath, contentFormat = 'JSON'):
    validateContentFormat(contentFormat)
    try:
        tokenString = ""
        endPoint = urllib3.util.parse_url(zestClient.endpoint)
        tokenString = arbiterClient.requestToken(endPoint.host, tokenPath, "GET")
        print("Token Received for GET")
        print(tokenString)
        response = zestClient.get(path, contentFormat, tokenString)
        print("Response received from get")
        print(response)
        if(response is not None and contentFormat == 'JSON'):
            response = json.loads(response)
            print(response)
        return response

    except ValueError:
        print("Read Error: for path " + ValueError)



def _write(arbiterClient, zestClient, path, tokenPath, payload, contentFormat = 'JSON'):
    validateContentFormat(contentFormat)
    print(type(payload))
    if(payload is not None and  type(payload )=='object'  and  contentFormat == 'JSON'):
        try:
            payload = json.dumps(payload)
        except ValueError:
            print("Write Error: invalid json payload " + ValueError)

    try:
        endPoint = urllib3.util.parse_url(zestClient.endpoint)
        print("endpoint + " + str(endPoint.host))
        print("token path" + str(tokenPath))
        token = arbiterClient.requestToken(endPoint.host, tokenPath, "POST", [])
        print("token received from arbiter +" + str(token))
        if (token is None):
            #token = arbiter_token
            token = config.ARBITER_TOKEN#this is just for testing
        payload = str(payload)
        response = zestClient.post(path, payload, contentFormat, token)

        #Todo this is here to maintain backward compatibility after moving to zest should be removed
        if(response == ''):
            response = 'created'
        return response
    except ValueError:
        print("Write Error: for path " + ValueError)




def validateContentFormat(contentFormat):
    try:
        switcher = {"TEXT": True, "BINARY": True, "JSON": True}
        if switcher.get(contentFormat.upper()) == True:
            return True
        else:
            raise ValueError
    except ValueError:
        print("Error: Unsupported content format")




def __del__(self):
    self.store.closeSockets()


def  NewDataSourceMetadata():
     return {'Description': ' ',
             'ContentType': ' ',
             'Vendor': ' ',
             'DataSourceType': ' ',
             'DataSourceID': ' ',
             'StoreType': ' ',
             'IsActuator': False,
             'Unit': ' ',
             'Location': ' ',}

hostname = os.environ['DATABOX_LOCAL_NAME']
