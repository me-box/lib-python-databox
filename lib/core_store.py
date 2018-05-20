__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2017, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

#from pythonzestclient import *
import pythonzestclient.pyZestClient as zest
from lib import utils as utils
import urllib3



class NewKeyValueClient:
    def __init__(self, reqEndpoint, enableLogging):
        self.zestEndpoint = reqEndpoint
        self.zestDealerEndpoint = reqEndpoint.replace(":5555", ":5556")
        self.store = zest.PyZestClient(utils.CORE_STORE_KEY,self.zestEndpoint,self.zestDealerEndpoint)

    def _read(self, store,  storeEndpoint, path, tokenPath, contentFormat):
        tokenString = ""
        endPoint = urllib3.util.parse_url(storeEndpoint)
        tokenString = utils.requestToken(endPoint.host, tokenPath, "GET")
        results = store.get(path, contentFormat, tokenString)
        print(results)
        return results

    def read(self, dataSourceID, key, contentFormat):
        path = "/kv/" + dataSourceID + "/" + key
        return self._read(self.store,  self.zestEndpoint, path, path, contentFormat)

    def _write(self, store, storeEndpoint, path, tokenPath, payload, contentFormat):
        tokenString = ""
        endPoint = urllib3.util.parse_url(storeEndpoint)
        tokenString = utils.requestToken(endPoint.host, tokenPath, "POST")
        results = store.post(path, payload, contentFormat, tokenString)
        print(results)
        return results

    def write(self, dataSourceID, key, payload, contentFormat):
        path = "/kv/" + dataSourceID + "/" + key
        return self._write(self.store, self.zestEndpoint, path, path, payload, contentFormat)

    def __del__(self):
        self.store.closeSockets()

class NewTimeSeriesClient:
    def __init__(self, reqEndpoint, enableLogging):
        zestEndpoint = reqEndpoint
        zestDealerEndpoint = reqEndpoint.replace(":5555", ":5556")
        self.store = zest.PyZestClient(utils.CORE_STORE_KEY, zestEndpoint, zestDealerEndpoint)


    def _write(self, store, storeEndpoint, path, tokenPath, payload, contentFormat):
        tokenString = ""
        endPoint = urllib3.util.parse_url(storeEndpoint)
        tokenString = utils.requestToken(endPoint.host, tokenPath, "POST")
        results = store.post(path, payload, contentFormat, tokenString)
        return results

    def write(self, dataSourceID, payload, contentFormat):
        path = "/ts/blob/" + dataSourceID
        return self._write(self.store, self.zestEndpoint, path, path, payload, contentFormat)

    def _read(self, store, storeEndpoint, path, tokenPath, contentFormat):
        tokenString = ""
        endPoint = urllib3.util.parse_url(storeEndpoint)
        tokenString = utils.requestToken(endPoint.host, tokenPath, "GET")
        results = store.get(path, contentFormat, tokenString)
        return results


    def latest(self,dataSourceID, contentFormat):
        path = "/ts/blob/" + dataSourceID + "/latest"
        return self._read(self.store, self.zestEndpoint, path, path, contentFormat)



    def length(self,dataSourceID, key, contentFormat):
        print("length")

    def lastN(self):
        print("lastN")

    def firstN(self):
        print("firstN")

    def range(self):
        print("range")

    def __del__(self):
        print("del")
    #self.store.closeSockets()










