from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import threading
from wpwithin.WPWithinCallback import Client
from wpwithin.WPWithinCallback import Processor

class CallbackHandler:
    def __init__(self):
        self.log = {}

    def beginServiceDelivery(self, serviceId, serviceDeliveryToken, unitsToSupply):
        try:
            print "event from core - onBeginServiceDelivery()"
            print "ServiceID: {0}\n".format(serviceId)
            print "UnitsToSupply: {0}\n".format(unitsToSupply)
            print "SDT.Key: {0}\n".format(serviceDeliveryToken.key)
            print "SDT.Expiry: {0}\n".format(serviceDeliveryToken.expiry)
            print "SDT.Issued: {0}\n".format(serviceDeliveryToken.issued)
            print "SDT.Signature: {0}\n".format(serviceDeliveryToken.signature)
            print "SDT.RefundOnExpiry: {0}\n".format(serviceDeliveryToken.refundOnExpiry)
        except Exception as e:
            print "doBeginServiceDelivery failed: " + str(e)

    def endServiceDelivery(self, serviceId, serviceDeliveryToken, unitsReceived):
        try:
	        print "event from core - onEndServiceDelivery()"
	        print "ServiceID: {0}\n".format(serviceId)
	        print "UnitsReceived: {0}\n".format(unitsReceived)
	        print "SDT.Key: {0}\n".format(serviceDeliveryToken.key)
	        print "SDT.Expiry: {0}\n".format(serviceDeliveryToken.expiry)
	        print "SDT.Issued: {0}\n".format(serviceDeliveryToken.issued)
	        print "SDT.Signature: {0}\n".format(serviceDeliveryToken.signature)
	        print "SDT.RefundOnExpiry: {0}\n".format(serviceDeliveryToken.refundOnExpiry)
        except Exception as e:
	        print "doEndServiceDelivery failed: " + str(e)

    def makePaymentEvent(self, totalPrice, orderCurrency, clientToken, orderDescription, uuid):
        try:
            print "event from core - onMakePaymentEvent()"
            print "totalPrice: {0}\n".format(totalPrice)
            print "orderCurrency: {0}\n".format(orderCurrency)
            print "clientToken: {0}\n".format(clientToken)
            print "orderDescription: {0}\n".format(orderDescription)
            print "uuid: {0}\n".format(uuid)
        except Exception as e:
            print "onMakePaymentEvent failed: " + str(e)

    def serviceDiscoveryEvent(self, remoteAddr):
        try:
            print "event from core - onServiceDiscoveryEvent()"
            print "remoteAddr: {0}\n".format(remoteAddr)
        except Exception as e:
            print "onServiceDiscoveryEvent failed: " + str(e)

    def servicePricesEvent(self, remoteAddr, serviceId):
        try:
            print "event from core - onServicePricesEvent()"
            print "remoteAddr: {0}\n".format(remoteAddr)
            print "serviceId: {0}\n".format(serviceId)
        except Exception as e:
            print "onServicePricesEvent failed: " + str(e)

    def serviceTotalPriceEvent(self, remoteAddr, serviceID, totalPriceResp):
        try:
            print "event from core - onServiceTotalPriceEvent()"
            print "remoteAddr: {0}\n".format(remoteAddr)
            print "serviceId: {0}\n".format(serviceID)
            print "totalPriceResp: {0}\n".format(totalPriceResp)
        except Exception as e:
            print "onServiceTotalPriceEvent failed: " + str(e)

    def errorEvent(self, msg):
        try:
            print "event from core - onErrorEvent()"
            print "msg: {0}\n".format(msg)
        except Exception as e:
            print "onErrorEvent failed: " + str(e)

class EventServer:
    server = None

    def startServer(self, server):
    	print "##### STARTING WRAPPER SERVER to receive callbacks #####"
    	print "##### SERVER: " + str(server)
    	server.serve()

    def stop():
        if server != None:
            server.setShouldStop(True)

    def __init__(self, listenerHandler, hostname, port):
        try:
            if(listenerHandler == None):
                print "Using build-in handler"
                theListenerToUse = CallbackHandler()
            else:
                print "Using custom handler"
                theListenerToUse = listenerHandler
            processor = Processor(theListenerToUse)
            transport = TSocket.TServerSocket(host=hostname, port=port)
            tfactory = TTransport.TBufferedTransportFactory()
            pfactory = TBinaryProtocol.TBinaryProtocolFactory()
            #self.server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
            self.server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
            print "Serving the Wrapper listener, port: " + str(port)
            thread = threading.Thread(target=self.startServer, args=([self.server]))
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution
            print "##### SERVER: " + str(self.server)
            print "##### SERVER: SHOULD HAVE STARTED"
            print "Should have started Wrapper listener"
        except Exception as e:
            print "Event server setup failed: " + str(e)


