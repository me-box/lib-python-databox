__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

from pythonzestclient.pyZestClient import pyZestClient as zestclient

class NewKeyValueClient:
    def __init__(self, reqEndpoint, enableLogging):
        self.store = zestclient('vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<',reqEndpoint, "tcp://127.0.0.1:5556")

    def _read(self, store, path, tokenPath, contentFormat):
        results = store.get(path, contentFormat, tokenString="")
        return results

    def read(self, dataSourceID, key, contentFormat):
        path = "/kv/" + dataSourceID + "/" + key
        return self._read(self.store, path, path,contentFormat)

    def _write(self, store, path, tokenPath, payload, contentFormat):
        results = store.post(path, payload, contentFormat, tokenString="")
        return results

    def write(self, dataSourceID, key, payload, contentFormat):
        path = "/kv/" + dataSourceID + "/" + key
        return self._write(self.store, path, path, payload, contentFormat)

    def __del__(self):
        self.store.closeSockets()

class NewTimeSeriesClient:
    def __init__(self, reqEndpoint, enableLogging):
        self.store = zestclient('vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<', reqEndpoint, "tcp://127.0.0.1:5556")


    def _write(self, store, path, tokenPath, payload, contentFormat):
        results = store.post(path, payload, contentFormat, tokenString="")
        return results

    def write(self, dataSourceID, payload, contentFormat):
        path = "/ts/blob/" + dataSourceID
        return self._write(self.store, path, path, payload, contentFormat)

    def _read(self, store, path, tokenPath, contentFormat):
        results = store.get(path, contentFormat, tokenString="")
        return results


    def latest(self,dataSourceID, contentFormat):
        path = "/ts/blob/" + dataSourceID + "/latest"
        return self._read(self.store, path, path, contentFormat)



    def length(self,dataSourceID, key, contentFormat):
        print("length")

    def lastN(self):
        print("lastN")

    def firstN(self):
        print("firstN")

    def range(self):
        print("range")

    def __del__(self):
        self.store.closeSockets()



def main():
    kv = NewKeyValueClient("tcp://127.0.0.1:5555", False)
    response = kv.read('newkey', 'test',contentFormat="JSON" )
    print("response received " + str(response))

    #p.get(tokenString="",path='/kv/newkey/test',contentFormat="JSON")
    kv.write("newkey","test1",'{"name":"testuser", "age":37}', contentFormat="JSON")
    response = kv.read('newkey', 'test1', contentFormat="JSON")
    print("response received " + str(response))

    ts = NewTimeSeriesClient("tcp://127.0.0.1:5555", False)
    ts.write("newkeyts", '{"name":"testuserts", "age":37}', contentFormat="JSON")
    response = ts.latest("newkeyts")
    print("response received " + str(response))

    #p.observe(tokenString="",path='/kv/test',contentFormat="JSON", timeOut=300)
    #p.post(tokenString="", path='/kv/test', payLoad='{"name":"testuser1", "age":35}', contentFormat="JSON")
    del kv
if __name__=="__main__":
    main()









