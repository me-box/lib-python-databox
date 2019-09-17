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

from pythonzestclient.exception.PyZestException import PyZestException


class PyZestClient:
    def __init__(self, server_key, end_point, dealer_endpoint, logger=None):
        """

        :param server_key:
        :param end_point:
        :param certificate_file - Client certificate file used to establish conn with the Server using CURVE zmq api
        """

        self.logger = logger or logging.getLogger(__name__) #get the Logger object
        self.logger.setLevel(logging.INFO) # set which kind of errors should be output (e.g. logging.INFO - starting from INFO severity level)
        self.serverKey = server_key #key to the ZEST db server, usually string
        self.endpoint = end_point #zest endpoint
        #vs451: added dealer_endpoint assignment
        self.dealer_endpoint = dealer_endpoint
        self.logger.debug("Connecting to the server")
        self.observers = {}
        #the TRY block describes connection establishment with the server and dealer_endpoint
        try:
            #connection with server
            ctx = zmq.Context()
            auth = ThreadAuthenticator(ctx) #runs authentification as a background thread within a specific context
            auth.start()
            auth.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY) #configure CURVE authentification for a given fomain ('*' - for all domains)
            self.socket = ctx.socket(zmq.REQ) #initialize request socket
            client_public, client_secret = zmq.curve_keypair()
            #assigning public and private keys to REQ socket
            self.socket.curve_secretkey = client_secret
            self.socket.curve_publickey = client_public

            self.socket.curve_serverkey = bytes(server_key, 'utf8')
            self.socket.connect(end_point)
            self.logger.info('Connection established with ' + end_point)

            #connection with dealer
            self.socket_d = ctx.socket(zmq.DEALER)


        except zmq.ZMQError as e:
            self.logger.error("Cannot establish connection" + str(e))


    def post(self,path, payLoad, contentFormat,tokenString=None):

        print("Inside post")

        self.logger.debug("Posting data to the endpoint")
        #return dictionary struct of header
        header = pyZestUtil.zestHeader()
        header["code"] = 2
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["payload"] = payLoad
        header["oc"] = 3
        print(len(tokenString))
        print("Token string received -- " + str(header["token"]))

        # set header options as an array of dictionaries
        options = []
        #append Uri-path
        options.append({"number":11,
        "len": len(path),
        "value": path,})
        #append Uri-host
        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})
        #append content format
        options.append({"number": 12,
                        "len": 2,
                        "value": pyZestUtil.content_format_to_int(contentFormat),})

        header["options"] = options
        # header marshal into bytes
        header_into_bytes = pyZestUtil.marshalZestHeader(header)


        try:
            response = self.send_request_and_await_response(header_into_bytes)
            print("response from send request " + str(response))
            try:
                parsed_response = self.handle_response(response, self.returnPayload)
                return parsed_response
            except (RuntimeError, TypeError, NameError) as e:
                self.logger.error("Inside Post: Error runtime or type or name - " +  str(e.args) )

        except ValueError as e:
            self.logger.error( "Inside Post: Message sending error - " +  str(e.args) )



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
            print("Respons from GET")
            print(response)
            try:
                parsed_response = self.handle_response(response,self.returnPayload)
                print(parsed_response)
                if parsed_response is None:
                    return parsed_response
                else:
                    return parsed_response
            except (RuntimeError, TypeError, NameError) as e:
                self.logger.error("Inside GET: Error runtime or type or name - " + str(e.args))

        except ValueError as e:
            self.logger.error("Inside GET: Message sending error - " + str(e.args))

    #vs451: added delete method
    def delete(self, path, contentFormat, tokenString=None):
        self.logger.debug("Inside DELETE: deleting data from the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 4
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
                if parsed_response is None:
                    return parsed_response
                else:
                    return parsed_response["payload"]
            except (RuntimeError, TypeError, NameError) as e:
                self.logger.error("Inside DELETE: Error runtime or type or name - " + str(e.args))

        except ValueError as e:
            self.logger.error("Inside DELETE: Message sending error - " + str(e.args))

    #vs451: added observeMode parameter ("data" or "audit" values)
    def observe(self, path, contentFormat, tokenString=None, observeMode = None, timeOut = 0):
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
        #Q: guess this is observe option("data" or "audit")
        options.append({"number": 6,
                    "len": len(observeMode), #vs451 added observe Mode len assignment
                    "value":observeMode,}) #vs451 added observe Mode value assignment
        options.append({"number": 12,
                    "len": 2,
                    "value": pyZestUtil.content_format_to_int(contentFormat),})
        #append Max-Age
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
            return parsed_response
        except Exception as e:
            self.logger.error("Inside Observe: Error in handling response: " + str(e.args[0]))
        #return 1 vs451: made observe method to return parsed_response instead of 1


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
            dealer.connect(self.dealer_endpoint)
            print("connected to dealer")
        except Exception as e:
            self.logger.error("Inside Resolve: Error connecting dealer - " + str(e.args))

        try:
            message = dealer.recv(0)
            #print(message)
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
        print("Inside handle response ", zr["code"])
        try:
            if zr["code"] == 65:
                return zr
            #vs451: added delete response code
            elif zr["code"] == 66:
                return fun(zr)
            elif zr["code"] == 69:
                #commented two following lines as want the method to return payload
                #pl = fun(zr)
                #return zr["payload"]
                return fun(zr)
            elif zr["code"]== 128:
                # Code 128 corresponds to bad request
                raise PyZestException(zr, "Bad Request")
            elif zr["code"] == 129:
                raise PyZestException(zr, "Unauthorized request")
            elif zr["code"] == 143:
                raise PyZestException(zr, "UnSupported content format")
            else:
                raise PyZestException(zr, "Invalid code" + str(zr["code"])) 

        except PyZestException as e:
            self.logger.error("received incorrect request " + str(e.args))

    def returnPayload(self, x):
        return x["payload"]

    def returnInput(self, x):
        return x

    def closeSockets(self):
        self.socket.close()

    def stopObserving(self):
        pass
