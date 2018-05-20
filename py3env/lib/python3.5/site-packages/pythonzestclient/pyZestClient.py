__author__ = 'pooyadav'

import logging
import struct
import os

import binascii
import zmq

import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

from pythonzestclient import pyZestUtil
import socket as sc


from pythonzestclient.exception.pyZestException import PyZestException


class PyZestClient:
    def __init__(self, server_key, end_point, dealer_endpoint, logger=None):
        """

        :param server_key:
        :param end_point:
        :param certificate_file - Client certificate file used to establish conn with the Server using CURVE zmq api
        """

        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.serverKey = server_key
        self.endpoint = end_point
        self.logger.debug("Connecting to the server")
        self.observers = {}
        try:
            ctx = zmq.Context()
            auth = ThreadAuthenticator(ctx)
            auth.start()
            auth.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)
            self.socket = ctx.socket(zmq.REQ)
            client_public, client_secret = zmq.curve_keypair()
            self.socket.curve_secretkey = client_secret
            self.socket.curve_publickey = client_public

            self.socket.curve_serverkey = bytes(server_key, 'utf8')
            self.socket.connect(end_point)
            self.logger.info('Connection established with ' + end_point)

        except zmq.ZMQError as e:
            self.logger.error("Cannot establish connection" + str(e.args))


    def post(self,path, payLoad, contentFormat,tokenString=None):

        self.logger.debug("Posting data to the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 2
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["payload"] = payLoad
        header["oc"] = 3


        # set header options
        options = []
        options.append({"number":11,
        "len": len(path),
        "value": path,})

        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})

        options.append({"number": 12,
                        "len": 2,
                        "value": pyZestUtil.content_format_to_int(contentFormat),})

        header["options"] = options
        # header marshal into bytes
        header_into_bytes = pyZestUtil.marshalZestHeader(header)

        try:
            response = self.send_request_and_await_response(header_into_bytes)
            try:
                parsed_response = self.handle_response(response, self.returnInput)
            except Exception as e:
                self.logger.error("Inside Post: Error in handling response - " + str(e.args))

                return parsed_response["payload"]
        except Exception as e:
            self.logger.error( "Inside Post: Message sending error - " + str(e.args))



    def get(self, path, contentFormat, tokenString=None):
        self.logger.debug("Inside GET: Getting data from the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 1
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["oc"] = 3



        # set header options
        options = []
        options.append({"number":11,
        "len": len(path),
        "value": path,})

        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})

        options.append({"number": 12,
                        "len": 2,
                        "value": pyZestUtil.content_format_to_int(contentFormat),})
        header["options"] = options

        # header marshal into bytes
        header_into_bytes = pyZestUtil.marshalZestHeader(header)

        try:
            response = self.send_request_and_await_response(header_into_bytes)
            try:
                parsed_response = self.handle_response(response,self.returnPayload)
            except Exception as e:
                self.logger.error("Inside GET: Error in handling response -" + str(e.args))
            return parsed_response
        except Exception as e:
            self.logger.error( "Inside GET: Message sending error  " + str(e.args))


    def observe(self, path, contentFormat, tokenString=None, timeOut = 0):
        self.logger.debug("Observing data from the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 1
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["oc"] = 5
        options = []
        options.append({"number": 11,
                        "len": len(path),
                        "value": path,})
        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})
        options.append({"number": 6,
                    "len": 0,
                    "value":"",})
        options.append({"number": 12,
                    "len": 2,
                    "value": pyZestUtil.content_format_to_int(contentFormat),})
        options.append({"number": 14,
                        "len": 4,
                        "value": timeOut,})
        header["options"] = options

        header_into_bytes = pyZestUtil.marshalZestHeader(header)
        try:
            response = self.send_request_and_await_response(header_into_bytes)
        except Exception as e:
            self.logger.error("Inside Observe: Message sending error - " + str(e.args))
        try:
            parsed_response = self.handle_response(response, self.resolve)
        except Exception as e:
            self.logger.error("Inside Observe: Error in handling response: " + str(e.args[0]))
        return 1


    def resolve(self, header):
        newCtx = zmq.Context()
        dealer = newCtx.socket(zmq.DEALER)
        if(dealer.closed):
            print("Dealer Closed")
        else:
            print("Dealer is Open")
        try:
            dealer.setsockopt_string(zmq.IDENTITY, header["payload"])
            #dealer.identity = str(header["payload"])
        except Exception as e:
            self.logger.error("Inside Resolve: Error setting identity - " + str(e.args))

        serverKey = ""
        for i in range(len(header["options"])):
            if(header["options"][i]["number"] == 2048):
                serverKeyOption = header["options"][i]
                serverKey = serverKeyOption["value"]

        try:
            client_public, client_secret = zmq.curve_keypair()
        except Exception as e:
            self.logger.error("Inside Resolve: Error getting keypair - " + str(e.args))

        try:
            dealer.curve_secretkey = client_secret
            dealer.curve_publickey = client_public
        except Exception as e:
            self.logger.error("Inside Resolve: Error setting dealer Public/Private keys - " + str(e.args))
        try:
            dealer.curve_serverkey = bytes(serverKey.encode('ascii'))

        except Exception as e:
            self.logger.error("Inside Resolve: Error setting dealer Server key - " + str(e.args))
        try:
            dealer.connect(dealer_endpoint)
        except Exception as e:
            self.logger.error("Inside Resolve: Error connecting dealer - " + str(e.args))

        try:
            message = dealer.recv(0)
        except Exception as e:
            self.logger.error("Inside resolve: Didn't get reponse " + str(e.args))
        parsed_response  = self.handle_response(message,self.returnPayload)
        return parsed_response

    def send_request_and_await_response(self, request):
        self.logger.info(" Sending request ...")
        try:
            if self.socket.closed:
                self.logger.error("No active connection")
            else:
                try:
                    self.socket.send(request,flags=0)
                except Exception as e:
                    self.logger.error("Error appeared " + str(e.args))
                try:
                    response = self.socket.recv(flags=0)
                    return response
                except Exception as e:
                    self.logger.error("Didn't get reponse " + str(e.args))
        except Exception as e:
            self.logger.error("Cannot send request " + str(e.args))


    def handle_response(self, msg, fun):
        """

        :param msg: Response from the server

        """
        self.logger.info(" Inside Handle Response...")
        zr = pyZestUtil.parse(msg)
        try:
            if zr["code"] == 65:
                return zr
            elif zr["code"] == 69:
                x = fun(zr)
                return 0
            elif zr["code"]== 128:
                # Code 128 corresponds to bad request
                raise PyZestException(zr, "Bad Request")
            elif zr["code"] == 129:
                raise PyZestException(zr, "Unauthorized request")
            elif zr["code"] == 143:
                raise PyZestException(zr, "UnSupported content format")
            else:
                raise PyZestException(zr, "Invalid code" + str(zr.code))

        except PyZestException as e:
            self.logger.error("Cannot parse the message " + str(e.args))

    def returnPayload(self, x):
        return x["payload"]
    def returnInput(self, x):
        return x
    def closeSockets(self):
        self.socket.close()
    def stopObserving(self):
        pass



