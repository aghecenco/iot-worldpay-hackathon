import logging

class WWTotalPriceResponse(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWPrice')

    def setServerId(self, serverId):
        self.serverId = serverId

    def setClientId(self, clientId):
        self.clientId = clientId

    def setPriceId(self, priceId):
        self.priceId = priceId

    def setUnitsToSupply(self, unitsToSupply):
        self.unitsToSupply = unitsToSupply

    def setTotalPrice(self, totalPrice):
        self.totalPrice = totalPrice

    def setPaymentReferenceId(self, paymentReferenceId):
        self.paymentReferenceId = paymentReferenceId

    def setMerchantClientKey(self, merchantClientKey):
        self.merchantClientKey = merchantClientKey

    def getServerId(self):
        return self.serverId

    def getClientId(self):
        return self.clientId

    def getPriceId(self):
        return self.priceId

    def getUnitsToSupply(self):
        return self.unitsToSupply

    def getTotalPrice(self):
        return self.totalPrice

    def getPaymentReferenceId(self):
        return self.paymentReferenceId

    def getMerchantClientKey(self):
        return self.merchantClientKey


class WWServiceMessage(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWServiceMessage')

    def setDeviceName(self, deviceName):
        self.deviceName = deviceName

    def setDeviceDescription(self, deviceDescription):
        self.deviceDescription = deviceDescription

    def setHostname(self, hostname):
        self.hostname = hostname

    def setPortNumber(self, portNumber):
        self.portNumber = portNumber

    def setServerId(self, serverId):
        self.serverId = serverId

    def setUrlPrefix(self, urlPrefix):
        self.urlPrefix = urlPrefix

    def setScheme(self, scheme):
        self.scheme = scheme

    def setServiceTypes(self, serviceTypes):
        self.serviceTypes = serviceTypes

    def getDeviceName(self):
        return self.deviceName
        
    def getDeviceDescription(self):
        return self.deviceDescription

    def getHostname(self):
        return self.hostname

    def getPortNumber(self):
        return self.portNumber

    def getServerId(self):
        return self.serverId

    def getUrlPrefix(self):
        return self.urlPrefix

    def getScheme(self):
        return self.scheme

    def getServiceTypes(self):
        return self.serviceTypes

class WWServiceDetails(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWServiceDetails')

    def setServiceId(self, serviceId):
        self.serviceId = serviceId

    def setServiceDescription(self, serviceDescription):
        self.serviceDescription = serviceDescription

    def getServiceId(self):
        return self.serviceId

    def getServiceDescription(self):
        return self.serviceDescription


class WWServiceDeliveryToken(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)
    
    def __init__(self):
        logging.info('initialised WWService')

    def setKey(self, key):
        self.key = key

    def setIssued(self, issued):
        self.issued = issued

    def setExpiry(self, expiry):
        self.expiry = expiry

    def setRefundOnExpiry(self, refundOnExpiry):
        self.refundOnExpiry = refundOnExpiry

    def setSignature(self, signature):
        self.signature = signature

    def getKey(self):
        return self.key

    def getIssued(self):
        return self.issued

    def getExpiry(self):
        return self.expiry

    def getRefundOnExpiry(self):
        return self.refundOnExpiry

    def getSignature(self):
        return self.signature


class WWService(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)
    # name = None
    # description = None
    # theId = None
    # prices = None
    # name = None
    # description = None

    def __init__(self):
        logging.info('initialised WWService')
        self.serviceType = None

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setId(self, theId):
        self.theId = theId

    def setServiceType(self, serviceType):
        self.serviceType = serviceType

    def setPrices(self, prices):
        self.prices = prices

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getId(self):
        return self.theId

    def getServiceType(self):
        return self.serviceType

    def getPrices(self):
        return self.prices


class WWPricePerUnit(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWPricePerUnit')

    def setAmount(self, amount):
        self.amount = amount

    def setCurrencyCode(self, currencyCode):
        self.currencyCode = currencyCode

    def getAmount(self):
        return self.amount

    def getCurrencyCode(self):
        return self.currencyCode


class WWPrice(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWPrice')

    def setId(self, id):
        self.id = id

    def setDescription(self, description):
        self.description  = description

    def setUnitDescription(self, unitDescription):
        self.unitDescription = unitDescription

    def setUnitId(self, unitId):
        self.unitId = unitId

    def setPricePerUnit(self, pricePerUnit):
        self.pricePerUnit = pricePerUnit

    def getId(self):
        return self.id

    def getDescription(self):
        return self.description

    def getUnitDescription(self):
        return self.unitDescription

    def getUnitId(self):
        return self.unitId

    def getPricePerUnit(self):
        return self.pricePerUnit


class WWPaymentResponse(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWPaymentResponse')

    def setServerId(self, serverId):
        self.serverId = serverId

    def setClientId(self, clientId):
        self.clientId = clientId

    def setTotalPaid(self, totalPaid):
        self.totalPaid = totalPaid

    def setServiceDeliveryToken(self, serviceDeliveryToken):
        self.serviceDeliveryToken = serviceDeliveryToken

    def setClientUuid(self, clientUuid):
        self.clientUuid = clientUuid

    def getServerId(self):
        return self.serverId

    def getClientId(self):
        return self.clientId

    def getTotalPaid(self):
        return self.totalPaid

    def getServiceDeliveryToken(self):
        return self.serviceDeliveryToken

    def getClientUuid(self):
        return self.clientUuid


class WWHCECard(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWHCECard')

    def setFirstName(self, firstName):
        self.firstName = firstName

    def setLastName(self, lastName):
        self.lastName = lastName

    def setCardNumber(self, cardNumber):
        self.cardNumber = cardNumber

    def setExpMonth(self, expMonth):
        self.expMonth = expMonth

    def setExpYear(self, expYear):
        self.expYear = expYear

    def setType(self, type):
        self.type = type

    def setCvc(self, cvc):
        self.cvc = cvc

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def getExpMonth(self):
        return self.expMonth

    def getExpYear(self):
        return self.expYear

    def getCardNumber(self):
        return self.cardNumber

    def getType(self):
        return self.type

    def getCvc(self):
        return self.cvc


class WWDevice(object):
    logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

    def __init__(self):
        logging.info('initialised WWDevice')

    def setUid(self, uid):
        self.uid = uid

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description  = description

    def setServices(self, services):
        self.services = services

    def setUnitDescription(self, unitDescription):
        self.unitDescription = unitDescription

    def setIpv4Address(self, ipv4Address):
        self.ipv4Address = ipv4Address

    def setCurrencyCode(self, currencyCode):
        self.currencyCode = currencyCode

    def getUid(self):
        return self.uid

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getServices(self):
        return self.services

    def getIpv4Address(self):
        return self.ipv4Address

    def getCurrencyCode(self):
        return self.currencyCode


class WPWithinGeneralException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)
        # Now for your custom code...
        self.errors = errors
