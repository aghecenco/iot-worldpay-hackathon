import wpwithinpy.WPWithinWrapperImpl as WPWithinWrapperImpl
import wpwithinpy.WWTypes as WWTypes
import time
import os
import sys

def killTheRpcAgent():
    print "Will attempt to kill the rpc-agent - this will now be handled by the SDK"
    killCommand = "ps aux | grep -i 'rpc-agent.*port.*8778' | awk '{print $2}' | xargs kill -9"
    # Finding the process based on the port number is safer than relying on the pid number that it was started on
    os.system(killCommand)

def discoverDevices(): # throws WPWithinGeneralException {
    devices = wpw.deviceDiscovery(8000)
    if devices != None and len(devices) > 0: 
        print "{0} services found:\n".format(len(devices))
        for svcMsg in devices:
            print "Device Description: {0}\n".format(svcMsg.getDeviceDescription())
            print "Hostname: {0}\n".format(svcMsg.getHostname())
            print "Port: {0}\n".format(svcMsg.getPortNumber())
            print "URL Prefix: {0}\n".format(svcMsg.getUrlPrefix())
            print "ServerId: {0}\n".format(svcMsg.getServerId())
            print "Scheme: {0}\n".format(svcMsg.getScheme()) # debb kev this has gone missing...?
            print "--------"
    else:
        if devices != None:
            print "No services found... devices was None"
        else:
            print "No services found... devices length: " + len(devices)
    return devices

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

def getAvailableServices(): #throws WPWithinGeneralException {
    services = wpw.requestServices()
    print "{0} services found\n".format(len(services))
    if services != None and len(services) > 0:
        for svc in services:
            print "Service:"
            print "Id: {0}\n".format(svc.getServiceId())
            print "Description: {0}\n".format(svc.getServiceDescription())
            print "------"
    return services

def getServicePrices(serviceId): # throws WPWithinGeneralException {
    prices = wpw.getServicePrices(serviceId)
    print "{1} prices found for service id {1}\n".format(len(prices), serviceId)
    if prices != None and len(prices) > 0:
        for price in prices:
            print "Price: {0:.2f}".format(float(price.pricePerUnit.amount) / float(100))
            print "CurrencyCode: " + price.pricePerUnit.currencyCode
            print "Id: {0}\n".format(price.getId())
            print "Description: {0}\n".format(price.getDescription())
            print "UnitId: {0}\n".format(price.getUnitId())
            #print "UnitDescription: {0}\n".format(price.getUnitDescription()) #not likey this some reason
            #print "Unit Price Amount: {10.2f}\n".format(price.getPricePerUnit().getAmount()) #not likey this... :(
            #print "Unit Price CurrencyCode: {0}\n".format(price.getPricePerUnit().getCurrencyCode()) #not likey this either...
            print "------"
    return prices

def getServicePriceQuote(serviceId, numberOfUnits, priceId): # throws WPWithinGeneralException {
    tpr = wpw.selectService(serviceId, numberOfUnits, priceId)
    if tpr != None:
            print "Did retrieve price quote:"
            print "Merchant client key: {0}\n".format(tpr.getMerchantClientKey())
            print "Payment reference id: {0}\n".format(tpr.getPaymentReferenceId())
            print "Units to supply: {0}\n".format(tpr.getUnitsToSupply())
            #print "Currency code: {0}\n".format(tpr.getCurrencyCode()) #TODO fix this
            print "Total price: {0:.2f}\n".format(float(tpr.getTotalPrice())/float(100))
    else:
        print "Result of select service is None"
    return tpr

def purchaseService(serviceId, pReq, numberOfUnits): # throws WPWithinGeneralException {
    pResp = wpw.makePayment(pReq)
    sdt = pResp.getServiceDeliveryToken()
    if pResp != None:

            print 'Payment response:'
            print "Total paid: {0:.2f}\n".format(float(pResp.getTotalPaid())/float(100))
            print "ServiceDeliveryToken.issued: {0}\n".format(sdt.getIssued()) #not coming through right
            print "ServiceDeliveryToken.expiry: {0}\n".format(sdt.getExpiry())
            print "ServiceDeliveryToken.key: %{0}\n".format(sdt.getKey())
            print "ServiceDeliveryToken.signature: {0}\n".format(sdt.getSignature())
            print "ServiceDeliveryToken.refundOnExpiry: {0}\n".format(sdt.getRefundOnExpiry())
            beginServiceDelivery(serviceId, sdt, numberOfUnits)
    else:
        print 'Result of make payment is None..'
    return pResp

def beginServiceDelivery(serviceID, token, unitsToSupply): # throws WPWithinGeneralException {
    print 'Calling beginServiceDelivery()'
    print str(token)
    if token == None:
        print "Token empty at runConsumer side"
    else:
        print "Token not empty at runConsumer side"
    wpw.beginServiceDelivery(serviceID, token, unitsToSupply)
    try:
        print 'Sleeping 10 seconds..'
        time.sleep(10)
        endServiceDelivery(serviceID, token, unitsToSupply)
    except InterruptedException as e:
        print e

def endServiceDelivery(serviceID, token, unitsReceived): # throws WPWithinGeneralException {
    print 'Calling endServiceDelivery()'
    wpw.endServiceDelivery(serviceID, token, unitsReceived)

def run():
    print 'Starting Consumer Example Written in Python.'
    global wpw
    wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
    try:
        deviceName = "consumerDeviceTest"
        deviceDescription = "Consumer Device Tester"

        deviceNameInput = raw_input("deviceName=[" + deviceName + "] change or enter to leave unchanged: ")
        if deviceNameInput != "":
            deviceName = deviceNameInput

        deviceDescriptionInput = raw_input("deviceDescription=[" + deviceDescription + "] change or enter to leave unchanged: ")
        if deviceDescriptionInput != "":
            deviceDescription = deviceDescriptionInput

        confirm = raw_input("Next step 'wpw.setup(\'" + deviceName + "\',\'" + deviceDescription + "\') - (Y/N)")
        if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
            print "Okay exiting Flow Tester, bye"
            killTheRpcAgent()
            sys.exit(0)
        elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):
            wpw.setup(deviceName, deviceDescription)
            print "Successful ran 'wpw.setup(\'" + deviceName + "\',\'" + deviceDescription + "\')"
            confirm = raw_input("Next step 'wpw.getDevice()' - (Y/N)")
            if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                print "Okay exiting Flow Tester, bye"
                killTheRpcAgent()
                sys.exit(0)
            elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):
                wpwDevice = wpw.getDevice()
                print "Successful ran 'wpw.getDevice()'"
                print "::" + wpwDevice.getUid() + ":" + wpwDevice.getName() + ":" + wpwDevice.getDescription() + ":" + str(wpwDevice.getServices()) + ":" + wpwDevice.getIpv4Address() + ":" + wpwDevice.getCurrencyCode()
                if wpwDevice != None:
                    print "Successfully got a device"

                    confirm = raw_input("Next step 'wpw.deviceDiscovery(8000)' - (Y/N)")
                    if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                        print "Okay exiting Flow Tester, bye"
                        killTheRpcAgent()
                        sys.exit(0)
                    elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):

                        devices = discoverDevices()    
                        if devices != None:
                            onlyRunOnce = 0

                            print "[" + str(len(devices)) + "] devices discovered"


                            for svcMsg in devices:

                                confirm = raw_input("Next step 'wpw.initConsumer(\"http://\", " + svcMsg.getHostname() + ", " + str(svcMsg.getPortNumber()) + ", " + svcMsg.getUrlPrefix() + ", " + svcMsg.getServerId() + ", card, {\"psp_name\":\"worldpayonlinepayments\",\"api_endpoint\":\"https://api.worldpay.com/v1\"})' - (Y/N)")
                                if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                                    print "Okay exiting Flow Tester, bye"
                                    killTheRpcAgent()
                                    sys.exit(0)
                                elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):
                                    connectToDevice(svcMsg)

                                    print "Successfully connected to device"
                                    confirm = raw_input("Next step 'wpw.requestServices()' - (Y/N)")
                                    if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                                        print "Okay exiting Flow Tester, bye"
                                        killTheRpcAgent()
                                        sys.exit(0)
                                    elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):


                                        svcDetails = getAvailableServices()

                                        if svcDetails != None:

                                            print "[" + str(len(svcDetails)) + "] Successfully got services"
                                            confirm = raw_input("Next step 'wpw.getServicePrices(serviceId)' - (Y/N)")
                                            if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                                                print "Okay exiting Flow Tester, bye"
                                                killTheRpcAgent()
                                                sys.exit(0)
                                            elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):

                                                for svcDetail in svcDetails:

                                                    print "Getting services [" + str(svcDetail.getServiceId()) + "]"

                                                    confirm = raw_input("Next step 'wpw.getServicePrices(" + str(svcDetail.getServiceId()) + ")' - (Y/N)")
                                                    if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                                                        print "Okay exiting Flow Tester, bye"
                                                        killTheRpcAgent()
                                                        sys.exit(0)
                                                    elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):


                                                        svcPrices = getServicePrices(svcDetail.getServiceId())
                                                        if svcPrices != None:
                                                            print "[" + str(len(svcPrices)) +"] service prices received"
                                                            for svcPrice in svcPrices:
                                                                
                                                                howManyUnits = 6
                                                                howManyUnitsInput = raw_input("howManyUnits=[" + str(howManyUnits) + "] change or enter to leave unchanged: ")
                                                                if howManyUnitsInput != "":
                                                                    howManyUnits = int(howManyUnitsInput)

                                                                #Select the first price in the list
                                                                tpr = getServicePriceQuote(svcDetail.getServiceId(), howManyUnits, svcPrice.getId())
                                                                print 'Client ID: {0}\n'.format(tpr.getClientId())
                                                                print 'Server ID: {0}\n'.format(tpr.getServerId())

                                                                confirm = raw_input("Next step make a payment? 'wpw.makePayment(pReq)' - (Y/N)")
                                                                if("Y" != confirm and "y" != confirm and "YES" != confirm and "yes" != confirm and "Yes" != confirm):
                                                                    print "Okay skipping this payment"
                                                                elif("Y" == confirm or "y" == confirm or "YES" == confirm or "yes" == confirm or "Yes" == confirm):
                                                                    paymentResponse = purchaseService(svcDetail.getServiceId(), tpr, howManyUnits)
                                                                    confirm = raw_input("Payment completed successfully' - any key to continue")
                    confirm = raw_input("Flow complete' - any key to exit")
                    killTheRpcAgent()
                    sys.exit(0)
                else:
                    print "Could not get device, therefore exiting, bye"
                    killTheRpcAgent()
                    sys.exit(0)
                wpw.stopRPCAgent()
    except WWTypes.WPWithinGeneralException as wpge:
        killTheRpcAgent()
        print wpge
    except Exception as wpge2:
        killTheRpcAgent()
        print wpge2
        
run()
