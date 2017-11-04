from wpwithinpy import WPWithinWrapperImpl
from wpwithinpy import WWTypes
import time
import jsoncfg
import signal
import sys

class TheEventListener():
    def __init__(self):
        print "Inialised custom event listener"

    def beginServiceDelivery(self, serviceId, servicePriceID, serviceDeliveryToken, unitsToSupply):
        try:
            print "OVERRIDE: event from core - onBeginServiceDelivery()"
            print "ServiceID: {0}\n".format(serviceId)
            print "ServicePriceID: {0}\n".format(servicePriceID)
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
            print "OVERRIDE: event from core - onEndServiceDelivery()"
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

global wpw
wpw = None

def signal_handler(signum, frame):
    print "Signal", signum, "caught, stopping RPC agent."
    if wpw is not None:
        wpw.stopRPCAgent()
    sys.exit(0)

def parse_prices(fname):
    ret = {}
    with open(fname) as f:
        content = f.readlines()
        i = 0
        while i < len(content):
            line = content[i]
            if line.startswith('id'):
                ccPrice = WWTypes.WWPrice()
                ccPrice.setId(int(line.split()[1]))
                ccPrice.setDescription(" ".join(content[i+1].split()[1:]))
                ccPrice.setUnitDescription(content[i+2].split()[1])
                ccPrice.setUnitId(int(content[i+3].split()[1]))
                price = int(content[i+4].split()[1])
                
                ppu = WWTypes.WWPricePerUnit()
                ppu.setAmount(price)
                ppu.setCurrencyCode("GBP")
                ccPrice.setPricePerUnit(ppu)

                ret[ccPrice.getId()] = ccPrice
                #print str(price) + " : " + str(ccPrice.getId()) + " " + ccPrice.getDescription() + " " + ccPrice.getUnitDescription() + " " + str(ccPrice.getUnitId())
            i = i + 5
    return ret

def run():
    try:
        # catch term/int signals
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        print "WorldpayWithin Sample Producer (with callbacks)..."
        global config
        global wpw

        print "Load configuration."
        config = jsoncfg.load_config('config/producerCallbacksOWP.json')

        wpWithinEventListener = TheEventListener()
        # add listeners to the events
        # wpWithinEventListener.onBeginServiceDelivery += doBeginServiceDelivery
        # wpWithinEventListener.onEndServiceDelivery += doEndServiceDelivery		
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl(config.host(), config.port(), True, wpWithinEventListener, 9095)
        wpw.setup("FunPay", "FunPay Events WorldpayWithin producer")		
        svc = WWTypes.WWService();
        svc.setName("Events Service")
        svc.setDescription("Can pay for your selected Event using Amazon Alexa")
        svc.setId(1)
        svc.setServiceType("FunPay")
        ccPrice = WWTypes.WWPrice()
        ccPrice.setId(1)
        ccPrice.setDescription("event")
        ccPrice.setUnitDescription("One event")
        ccPrice.setUnitId(1)
        ppu = WWTypes.WWPricePerUnit()
        ppu.setAmount(100)
        ppu.setCurrencyCode("GBP")
        ccPrice.setPricePerUnit(ppu)
        prices = {}
        prices[ccPrice.getId()] = ccPrice
        svc.setPrices(parse_prices("events.txt"))
        # [ CLIENT KEY, SERVICE KEY] : From online.worldpay.com
        wpw.initProducer(config.pspConfig())
        wpw.addService(svc)
        broadcastDuration = 20000
        durationSeconds = broadcastDuration / 1000
        wpw.startServiceBroadcast(broadcastDuration) #20000
        repeat = 0
        while repeat < durationSeconds:
            print "Producer Waiting " + str(durationSeconds - repeat) + " seconds to go..."
            time.sleep(1)
            repeat = repeat + 1
        print "Stopped broadcasting, RPC still running"
        repeat2 = 0
        while repeat2 < 99999999999:
            print "Producer keeping alive (to receive callbacks...)"
            time.sleep(1)
            repeat2 = repeat2 + 1        
    except WWTypes.WPWithinGeneralException as e:
        print "WPWithinGeneralException caught:", e
    except Exception as exc:
        print "Exception caught:", exc

run()
