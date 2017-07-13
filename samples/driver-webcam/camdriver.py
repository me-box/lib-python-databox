__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__email__ = "p.yadav@acm.org"

from flask import Flask, Response
import utils
import os
import sys
import ssl


runtime = get('Node')

app = Flask(__name__)

