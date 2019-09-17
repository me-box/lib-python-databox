__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2017, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

import urllib3
import os
import json
import base64
from urllib.parse import urlencode
import time
import socket
from dotenv import load_dotenv

try:
    DV = os.environ.get('DATABOX_VERSION')
except NameError:
    DV = None
else:
    if DV == None:
        print("Production run environment is not defined")
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        print("Setting test environment")
    else:
        print("Using production environment")


ARBITER_ENDPOINT = os.environ.get('DATABOX_ARBITER_ENDPOINT')
hostname = os.environ.get('DATABOX_LOCAL_NAME')or socket.getfqdn()

CORE_STORE_KEY = ''

if os.path.isfile('/run/secrets/ZMQ_PUBLIC_KEY'):
    with open('/run/secrets/ZMQ_PUBLIC_KEY') as f:
        CORE_STORE_KEY = f.read()
    f.close()
else:
    CORE_STORE_KEY = os.environ.get('CORE_STORE_KEY')
    print("'Warning: No ZMQ_PUBLIC_KEY provided so Databox will use the default key")

print(CORE_STORE_KEY)

ARBITER_TOKEN = ""

if(os.path.exists("/run/secrets/ARBITER_TOKEN")):
    arbiterToken = open("/run/secrets/ARBITER_TOKEN", "rb").read()
    arbiterTokenbase64 = base64.b64encode(arbiterToken)
elif (os.path.exists("/run/secrets/CM_KEY")):
    #we are running in the container manager
    arbiterToken = open("/run/secrets/CM_KEY", "rb").read()
    arbiterTokenbase64 = base64.b64encode(arbiterToken)
else:
    ARBITER_TOKEN = os.environ.get('ARBITER_TOKEN')

    print('Warning: Using default values for arbiterURL and arbiterToken')


CM_HTTPS_CA_ROOT_CERT = None
try:
    CM_HTTPS_CA_ROOT_CERT = open("/run/secrets/DATABOX_ROOT_CA").read()
except OSError:
    CM_HTTPS_CA_ROOT_CERT = None
else:
    if CM_HTTPS_CA_ROOT_CERT is not None:
        https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_cer='/run/secrets/DATABOX_ROOT_CA')
    else:
        http = urllib3.PoolManager()
        print('Warning: No HTTPS root certificate provided so Databox HTTPS certificates will not be checked')


def getHttpsCredentials():
    credentials = {}
    try:
       credentials = {"key": open("/run/secrets/DATABOX.pem").read() or '', "cert": open("/run/secrets/DATABOX.pem").read() or ''}
    except:
        print("Warning: No HTTPS certficate not provided HTTPS certificates missing.")
        credentials = {}
    return credentials

