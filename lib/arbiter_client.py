__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2017, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

import pythonzestclient.pyZestClient as zestClient
import lib.arbiter_token_cache as arbiterTokenCache
import lib.config as config
import json


def new_arbiter_client(reqEndpoint, enableLogging):
    return arbiter_client(reqEndpoint, enableLogging)

class arbiter_client:
    def __init__(self, reqEndpoint, enableLogging):
        self.requestTokenCache = {}
        self.config = config
        self.tokenCache = arbiterTokenCache.arbiter_token_cache()
        self.zestEndpoint = config.ARBITER_ENDPOINT
        self.zestDealerEndpoint = reqEndpoint.replace(":4444", ":4445")
        try:
            self.zestClient = zestClient.PyZestClient(config.CORE_STORE_KEY, self.zestEndpoint, self.zestDealerEndpoint,  False)
            print("Arbitor client Created")
        except IOError:
            print("zestclient didn't connect")





    def requestToken(self, targetHostname, path, method, caveat =[]):
        print(caveat)
        try:
            token = self.tokenCache.getCachedToken(targetHostname, path, method, caveat)
            if(token is False):
                print("False token from cached list")
            elif(token is None):
                print("Token received is None")
            else:
                return token

            token =  self.makeZestArbiterTokenRequest(targetHostname, path, method, caveat)
            print("Token Received")
            return token
        except ValueError:
                print("Error in getting token from zest arbiter")




    def makeZestArbiterTokenRequest(self, targetHostname, path, method, caveat = []):
        print("inside makeZestArbiter")
        self.req = {'target': targetHostname, 'path': path, 'method': method.upper(), 'caveats': []}
        if (caveat != None and type(caveat) == 'object'):
            self.req['caveats'] = [caveat]
        else:
            print("caveat is either none or not an object")
        reqJson = json.dumps(self.req)
        print(reqJson)

        try:
            token = self.zestClient.post('/token', reqJson, "JSON",self.config.ARBITER_TOKEN)
            print("insidezest -token just received   ")
            print(str(token))
            self.tokenCache.cacheToken(targetHostname, path, method, caveat, token)
            return token
        except ValueError:
                print('Error in getting token from zest client')










