#!/usr/bin/python

import ServiceAdapter
import EventServer
import rpc
import wpwithin.wpthrift_types
from wpwithin.WPWithin import Client
from wpwithin.wpthrift_types import ttypes
from wpwithin.wpthrift_types.ttypes import ServiceDeliveryToken
import time
import thrift
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import WWTypes
import logging
import socket




class WPWithinWrapperImpl(object):
    cachedClient = None
    rpcProcess = None
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self, ipAddress, portNumber, startRpcCallbackAgent=False, wpWithinEventListener=None, eventListenerPort=0):

        self.portNumber = portNumber
        self.ipAddress = ipAddress
        self.eventListenerPort = eventListenerPort
        if startRpcCallbackAgent != None and startRpcCallbackAgent != "" and startRpcCallbackAgent == True and eventListenerPort != None and eventListenerPort != "": 
            if eventListenerPort <= 0 or eventListenerPort > 65535:
                raise WWTypes.WPWithinGeneralException.WPWithinGeneralException("callback port must be >0 and <655535", None)
            eventServer = EventServer.EventServer(wpWithinEventListener, self.ipAddress, eventListenerPort)
        self.rpcRunning = False
        self.rpcProcess = self.startRpc(self.ipAddress, self.portNumber, self.eventListenerPort)
        self.setClientIfNotSet()


    def killRpcAgent(self):
        if self.rpcProcess is not None:
            self.rpcProcess.kill()

    def setClientIfNotSet(self):
		if self.cachedClient == None:
		    self.cachedClient = self.openRpcListener()

    def startRpc(self, ipAddress, port, eventListenerPort):
        # self.killRpcAgent()
        if(self.rpcRunning == False):
			logging.info("Starting Port: " + str(port))
			process = rpc.startRPC(ipAddress, port, eventListenerPort)
			self.rpcRunning = True
			#give time for the service to start
			time.sleep(5)
			return process

    def getClient(self):
		self.setClientIfNotSet()
		return self.cachedClient

    def openRpcListener(self):
        try:
            # Make socket
            transport = TSocket.TSocket(self.ipAddress, self.portNumber)
            # Buffering is critical. Raw sockets are very slow
            transport = TTransport.TBufferedTransport(transport)
            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            # Create a client to use the protocol encoder
            client = Client(protocol)
            # Connect!
            transport.open()
            logging.info("STARTED connection to SDK via RPC thrift")
            return client
        except Exception as e: 
            logging.info("Error: Couldn't open the RpcListener: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Error: Couldn't open the RpcListener", e)		    

    def setup(self, deviceName, deviceDescription):
        try:
	        self.getClient().setup(deviceName, deviceDescription)
	        logging.info("SHOULD HAVE SETUP DEVICE: (" + str(deviceName) + "), (" + str(deviceDescription) + ")")
        except Exception as e:
            logging.info("Error - Failure to setup DEVICE in the wrapper, could be the new config file is missing - gotcha!: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Error - Failure to setup DEVICE in the wrapper, could be the new config file is missing - gotcha!: ", e)

    def addService(self, theService):
        try:
            self.getClient().addService(ServiceAdapter.convertWWService(theService))
            logging.info('SHOULD HAVE ADDED SERVICE')
        except Exception as e:
            logging.info("Error - Add service to producer failed with Rpc call to the SDK lower level: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Error - Add service to producer failed with Rpc call to the SDK lower level", e)

    def removeService(self, svc):
        try:
            self.getClient().removeService(ServiceAdapter.convertWWService(svc))
        except Exception as e:
            logging.info("Removal of service failed in the wrapper: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Removal of service failed in the wrapper: ", e)

    def requestServices(self):
        try:
        	return ServiceAdapter.convertServiceDetailList(self.getClient().requestServices())
        except Exception as e: 
            logging.info("Request services failed in wrapper: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Request services failed in wrapper", e)               

    def getDevice(self):
        try:
            device = self.getClient().getDevice()
            wwDevice = ServiceAdapter.convertDevice(device)
            logging.info('SHOULD HAVE RUN GET DEVICE')
            return wwDevice
        except Exception as e: 
            logging.info("Get device in wrapper failed: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Get device in wrapper failed", e)                     


    def stopRPCAgent(self):
        logging.info('SHOULD STOP RPC AGENT')
        try:
            self.getClient().CloseRPCAgent()
        except socket.error as er:
            time.sleep(2)
            if self.rpcProcess is None or self.rpcProcess.poll() is not None:
                logging.info("RPC agent closed.")
            else:
                self.killRpcAgent()
                raise WWTypes.WPWithinGeneralException("RPC process killed.", er)
        except Exception as e:
            if self.rpcProcess is None or self.rpcProcess.poll() is not None:
                logging.info("RPC agent is closed.")
            else:
                self.killRpcAgent()
                raise WWTypes.WPWithinGeneralException("RPC process killed.", e)



    def deviceDiscovery(self, timeout):
        logging.info('STARTING DO DEVICE DISCOVERY')
        try:
            svcMsgs = ServiceAdapter.convertServiceMessages(self.getClient().deviceDiscovery(timeout))
            logging.info('Finished device discovery')
            return svcMsgs
        except Exception as e: 
            logging.info("Failed device discovery in wrapper: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Failed device discovery in wrapper", e)                     

    def searchForDevice(self, timeout, deviceName):
        logging.info("STARTING SEARCH FOR DEVICE")
        try:
            svcMsgs = ServiceAdapter.convertServiceMessage(self.getClient().searchForDevice(timeout, deviceName))
            logging.info("Finished searching for device: "+deviceName)
            return svcMsgs
        except Exception as e:
            logging.info("Failed search for device in wrapper: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Failed search for device in wrapper", e)

    def initConsumer(self, scheme, hostname, port, urlPrefix, serverId, hceCard, pspConfig):
        try:
		    self.getClient().initConsumer(scheme, hostname, port, urlPrefix, serverId, ServiceAdapter.convertWWHCECard(hceCard), pspConfig)
        except Exception as e: 
            logging.info("Initiating the consumer failed in the wrapper: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Initiating the consumer failed in the wrapper", e)   

    def initProducer(self, pspConfig):
        try:
            self.getClient().initProducer(pspConfig)
            logging.info('SHOULD HAVE INIT THE PRODUCER')
        except Exception as e: 
            logging.info("Initiating the producer failed in the wrapper: " + str(e))
            self.killRpcAgent()
            raise WWTypes.WPWithinGeneralException("Initiating the producer failed in the wrapper", e) 

    def startServiceBroadcast(self, timeout):
        try:
            self.getClient().startServiceBroadcast(timeout)
            logging.info('SHOULD HAVE START SERVICE BROADCAST')
        except WWTypes.WPWithinGeneralException as e:
            self.killRpcAgent()
            print "Start service broadcast in wrapper failed: " + e
        except Exception:
            self.killRpcAgent()            

    def stopServiceBroadcast(self):
        try:
            self.getClient().stopServiceBroadcast()
        except WWTypes.WPWithinGeneralException as e:
            self.killRpcAgent()
            print "Stop service broadcast failed: " + e
        except Exception:
            self.killRpcAgent()            

    def getServicePrices(self, serviceId):
    	try:
    	    return ServiceAdapter.convertServicePrices(self.getClient().getServicePrices(serviceId)) 
    	except WWTypes.WPWithinGeneralException as e:
            self.killRpcAgent()
            print "Get Service Prices failed in wrapper: " + e
        except Exception:
            self.killRpcAgent()            

    def selectService(self, serviceId, numberOfUnits, priceId):
    	try:
    	    return ServiceAdapter.convertTotalPriceResponse(self.getClient().selectService(serviceId, numberOfUnits, priceId))		
    	except WWTypes.WPWithinGeneralException as e:
            self.killRpcAgent()
     	    print "Select service failed in wrapper: " + e
        except Exception:
            self.killRpcAgent()            

    def makePayment(self, request):
        try:
            return ServiceAdapter.convertPaymentResponse(self.getClient().makePayment(ServiceAdapter.convertWWTotalPriceResponse(request)))
        except WWTypes.WPWithinGeneralException as e:
            self.killRpcAgent()
            print "Failed to make payment in the wrapper: " + e
        except Exception:
            self.killRpcAgent()

    def beginServiceDelivery(self, serviceId, serviceDeliveryToken, unitsToSupply):
        try:
            print "Checking ServiceDelviery Input"
            if(serviceId == None):
                raise WWTypes.WPWithinGeneralException('Service Id cant be None')
            elif(serviceDeliveryToken == None):
                raise WWTypes.WPWithinGeneralException('serviceDeliveryToken cant be None')
            elif(unitsToSupply == None):
                raise WWTypes.WPWithinGeneralException('unitsToSupply cant be None')
            else:
            	print "Input variables looked good " + str(serviceId) + " " + str(serviceDeliveryToken) + " " + str(unitsToSupply)
            csdt = ServiceAdapter.convertWWServiceDeliveryToken(serviceDeliveryToken)
            print "servicedeliverytoken converted: " + str(csdt)
            print "serviceId that's going to be consumed: " + str(serviceId)
            #sdt = self.getClient().beginServiceDelivery(str(clientId), ServiceDeliveryToken(key=serviceDeliveryToken.getKey(), issued="2019-01-02T15:04:05Z", expiry="2019-01-02T15:04:05Z", refundOnExpiry=False, signature="KEVSIG"), 3)
            sdt = self.getClient().beginServiceDelivery(serviceId, csdt, unitsToSupply)
            return ServiceAdapter.convertServiceDeliveryToken(sdt)
        except Exception as e:
            self.killRpcAgent()
            print "Failed to begin Service Delivery in the wrapper: " + str(e)
        #except WWTypes.WPWithinGeneralException as e:
        #    print "Failed to begin Service Delivery in the wrapper: " + e

    def endServiceDelivery(self, serviceId, serviceDeliveryToken, unitsReceived):
     	try:
     	    self.getClient().endServiceDelivery(serviceId, ServiceAdapter.convertWWServiceDeliveryToken(serviceDeliveryToken), unitsReceived)
    	except Exception as e:
            self.killRpcAgent()
    	    print "Failed to end Service Delivery in the wrapper: " + str(e)
