__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2017, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

import hashlib
import json

class arbiter_token_cache:
        def __init__(self):
            self.tokenCache = {}

        def invalidateToken(self, hostname, path, method, caveat):
            key = calculateCacheKey(hostname, path, method, caveat)
            if (key in self.tokenCache):
                del self.tokenCache[key]

        def cacheToken(self, hostname, path, method, caveat, token):
            key = calculateCacheKey(hostname, path, method, caveat)
            self.tokenCache[key] = token

        def getCachedToken(self, hostname, path, method, caveat):
            print("Inside getCachedToken\n")
            key = calculateCacheKey(hostname, path, method, caveat)
            if(key in self.tokenCache):
                return self.tokenCache[key]
            else:
                print("returning false")
                return False


def calculateCacheKey(hostname, path, method, caveat):
    print("Inside CalculateKey ")
    caveatJson = ""
    caveatJson = caveatToJson(caveat)

    print("received")
    print(type(caveatJson))
    combined_str = str(hostname) + str(path) + str(method) + str(caveatJson)
    print(combined_str )
    result = hashlib.md5(combined_str.encode())
    print("something")
    return result.hexdigest()

def caveatToJson(caveat):
    print("inside caveat to Json")
    caveatJson = ""
    print(type(caveat))
    if (caveat != None and  type(caveat) =='object'):
        caveatJson = json.dumps(caveat)
    return caveatJson















