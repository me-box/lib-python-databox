import lib.utils as utils
import urllib3
import json

#this function returns Datastore catalogs registers with the Arbiter.
def getRootCatalog():
	return utils.makeArbiterRequest('GET', '/cat', {'True': True})

# this function is CM-facing - so only be called from Container manager
def getStoreCatalog(href):
	rurl = urllib3.util.parse_url(href)
	newurl = rurl.scheme + ':' + '//' + rurl.host + ':' + str(rurl.port) + '/cat'
	return utils.makeStoreRequest(method = 'GET', jsonData={'True': True}, url=newurl)

#this function list all available stores.
def listAvailableStores():
	cat = getRootCatalog()
	cat = json.loads(cat.decode())
	list = {}
	storeList = []
	for item in cat['items']:
		for pair in item['item-metadata']:
			if (pair['rel'] == 'urn:X-hypercat:rels:hasDescription:en'):
				list["description"] = pair['val']
				list["hostname"] = urllib3.util.parse_url(item['href']).hostname
				list["href"] = item['href']
		storeList.append(list)
	return storeList

#this function is based on log-store
def walkStoreCatalogs():
	raise NotImplementedError

#this function is based on log-store
def mapStoreCatalogs():
	raise NotImplementedError


def registerDatasource(href, metadata):
	rurl = urllib3.util.parse_url(href)
	newurl = rurl.scheme + ':' + '//' + rurl.host + ':' + str(rurl.port)
	metadata = json.loads(metadata)
	cat = {
		"item-metadata": [{
					"rel": "urn:X-hypercat:rels:hasDescription:en",
					"val": metadata['description']
				}, {
					"rel": "urn:X-hypercat:rels:isContentType",
					"val": metadata['contentType']
				}, {
					"rel": "urn:X-databox:rels:hasVendor",
					"val": metadata['vendor']
				}, {
					"rel": "urn:X-databox:rels:hasType",
					"val": metadata['type']
				}, {
					"rel": "urn:X-databox:rels:hasDatasourceid",
					"val": metadata['datasourceid']
				}, {
					"rel": "urn:X-databox:rels:hasStoreType",
					"val": metadata['storeType']
				}],
        "href":  newurl+ '/' + metadata['datasourceid']
		}
	return utils.makeStoreRequest(method='POST', jsonData=cat, url=newurl+'/cat')


