import utils
import urllib3


def getRootCatalog():
    return utils.makeArbiterRequest('GET', '/cat', True)

def getStoreCatalog(href):
    rurl = urllib3.util.parse_url(href)
    newurl = rurl.scheme + ':' + '//' + rurl.host + ':' + str(rurl.port) + '/cat'
    return utils.makeStoreRequest(method = 'GET', url=newurl)

def listAvailableStores():
    return getRootCatalog()

def walkStoreCatalogs():
    getRootCatalog()

def mapStoreCatalogs():
    walkStoreCatalogs()


def registerDatasource(href, metadata):
    rurl = urllib3.util.parse_url(href)
    newurl = rurl.scheme + ':' + '//' + rurl.host + ':' + str(rurl.port)
    cat = {
			"item-metadata": [{
					"rel": "urn:X-hypercat:rels:hasDescription:en",
					"val": metadata.description
				}, {
					"rel": "urn:X-hypercat:rels:isContentType",
					"val": metadata.contentType
				}, {
					"rel": "urn:X-databox:rels:hasVendor",
					"val": metadata.vendor
				}, {
					"rel": "urn:X-databox:rels:hasType",
					"val": metadata.type
				}, {
					"rel": "urn:X-databox:rels:hasDatasourceid",
					"val": metadata.datasourceid
				}, {
					"rel": "urn:X-databox:rels:hasStoreType",
					"val": metadata.storeType
				}],
        newurl:  newurl+ '/' + metadata.datasourceid
		}

    return utils.makeStoreRequest(method='POST', json=cat, url=newurl+'/cat')


