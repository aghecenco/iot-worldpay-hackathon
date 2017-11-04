from wpwithinpy import WPWithinWrapperImpl
from wpwithinpy import WWTypes
import json
import time
import signal
import sys

global data2
data2 = []
global wpw
wpw = None

def connectToDevice(svcMsg): # throws WPWithinGeneralException {
    card = WWTypes.WWHCECard()
    card.setFirstName("Bilbo")
    card.setLastName("Baggins")
    card.setCardNumber("5555555555554444")
    card.setExpMonth(11)
    card.setExpYear(2018)
    card.setType("Card")
    card.setCvc("113")
    wpw.initConsumer("http://", svcMsg.getHostname(), svcMsg.getPortNumber(), svcMsg.getUrlPrefix(), svcMsg.getServerId(), card, {"psp_name":"worldpayonlinepayments","api_endpoint":"https://api.worldpay.com/v1"})

def resetJson():
    data3 = []
    try:
        with open('/Library/WebServer/Documents/worldpaywithin/device-scanner.json', 'w') as outfile:
            json.dump(data3, outfile)
    except Exception:
        print "You need to configure the webserver path if you want to output json"

def outputJson(svcMsg, numberOfServices):
    global data2
    data2 = data2 + [{    'serverid' : svcMsg.getServerId(),
                            'devicename' :svcMsg.getDeviceName(),
                            'devicedescription' : svcMsg.getDeviceDescription(),
                            'hostname' : svcMsg.getHostname(),
                            'portnumber' : svcMsg.getPortNumber(),
                            'urlprefix' : svcMsg.getUrlPrefix(),
                            'numberofservices' : numberOfServices,
                            }]
    try:
        with open('/Library/WebServer/Documents/worldpaywithin/device-scanner.json', 'w') as outfile:
            json.dump(data2, outfile)
    except Exception:
        print "You need to configure the webserver path if you want to output json"

def signal_handler(signum, frame):
    print "Signal", signum, "caught, stopping RPC agent."
    if wpw is not None:
        wpw.stopRPCAgent()
    sys.exit(0)

def scanOnce():
    global data2
    data2 = []
    #resetJson()
    flagScanTimeout = 9000
    print 'Starting Device Scanner Written in Python.'
    global wpw
    
    wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
    try:
        wpw.setup("kevingwp-pi", "Kevin Gordons Raspberry Pi - DEVICE SCANNER")
        wpwDevice = wpw.getDevice()

        deviceName = "Unimpl"
        try:
            deviceName = wpwDevice.getName()
        except Exception:
            print "Device name not yet implemented"
            deviceName = "Unimpl"
        if deviceName is None:
            deviceName = "Unimpl"

        print "::" + wpwDevice.getUid() + ":" + deviceName + ":" + wpwDevice.getDescription() + ":" + str(wpwDevice.getServices()) + ":" + wpwDevice.getIpv4Address() + ":" + wpwDevice.getCurrencyCode()
        print "Scanning network for devices now..."
        print "Will scan for " + str(flagScanTimeout) + " milliseconds\n"

        if wpwDevice != None:
            devices = wpw.deviceDiscovery(flagScanTimeout)    
            if devices != None:

                if len(devices) > 0:

                    print "------------------------------------------------------------"
                    print "Found " + str(len(devices)) + " devices\n"

                    

                    for svcMsg in devices:

                        connectToDevice(svcMsg)
                        svcDetails = wpw.requestServices()
                        numberOfServices = len(svcDetails)

                        deviceName2 = "Unimpl0"
                        try:
                            deviceName2 = svcMsg.getDeviceName()
                        except Exception as e:
                            print "Device name not yet implemented"
                            print(str(e))
                            deviceName2 = "Unimpl1"
                        if deviceName2 is None:
                            deviceName2 = "Unimpl2"
                        print "DeviceName:[" + deviceName2 + "] no-of-services:[" + str(numberOfServices) + "] [" + svcMsg.getServerId() + "] " + svcMsg.getDeviceDescription() + " @ " + svcMsg.getHostname() + ":" + str(svcMsg.getPortNumber()) + "" + svcMsg.getUrlPrefix() + "\n"					
                        outputJson(svcMsg, numberOfServices)

                    print "------------------------------------------------------------"
                else:
                    resetJson();
            else:
                resetJson();
                         
        wpw.stopRPCAgent()
    except WWTypes.WPWithinGeneralException as wpge:
        if wpw is not None:
            wpw.stopRPCAgent()
        print wpge
    except Exception as wpge2:
        if wpw is not None:
            wpw.stopRPCAgent()
        print wpge2
 
def run():
    # catch term/int signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        scanOnce()
        time.sleep(3)

run()
