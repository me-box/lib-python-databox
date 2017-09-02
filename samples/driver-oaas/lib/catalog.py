import utils
import urllib3


def getRootCatalog():
    return utils.makeArbiterRequest('GET', '/cat', True)

print("util imported")