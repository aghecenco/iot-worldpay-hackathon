import WWTypes

from wpwithin.wpthrift_types import ttypes
from wpwithin.wpthrift_types.ttypes import Device
from wpwithin.wpthrift_types.ttypes import HCECard
from wpwithin.wpthrift_types.ttypes import PaymentResponse
from wpwithin.wpthrift_types.ttypes import Price
from wpwithin.wpthrift_types.ttypes import PricePerUnit
from wpwithin.wpthrift_types.ttypes import Service
from wpwithin.wpthrift_types.ttypes import ServiceDetails
from wpwithin.wpthrift_types.ttypes import ServiceMessage
from wpwithin.wpthrift_types.ttypes import TotalPriceResponse
from wpwithin.wpthrift_types.ttypes import ServiceDeliveryToken

import logging

logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)

def convertWWHCECard(wwHceCard):
	logging.info('convertWWHCECard')
	return HCECard(firstName=wwHceCard.getFirstName(), lastName=wwHceCard.getLastName(), expMonth=wwHceCard.getExpMonth(), expYear=wwHceCard.getExpYear(), cardNumber=wwHceCard.getCardNumber(), type=wwHceCard.getType(), cvc=wwHceCard.getCvc())

def convertWWDevice(wwDevice):
	logging.info('convertWWDevice')
	return Device(uid=wwDevice.getUid(), name=wwDevice.getName(), description=wwDevice.getDescription(), services=wwDevice.getServices(), ipv4Address=wwDevice.getIpv4Address(), currencyCode=wwDevice.getCurrencyCode())

def convertWWPaymentResponse(wwPaymentResponse):
	logging.info('convertWWPaymentResponse')
	return PaymentResponse(serverId=wwPaymentResponse.getServerId(), clientId=wwPaymentResponse.getClientId(), totalPaid=wwPaymentResponse.getTotalPaid(), serviceDeliveryToken=convertWWServiceDeliveryToken(wwPaymentResponse.getServiceDeliveryToken()))

def convertWWPricePerUnit(wwPricePerUnit):
	logging.info('convertWWPricePerUnit')
	return PricePerUnit(amount=wwPricePerUnit.getAmount(), currencyCode=wwPricePerUnit.getCurrencyCode())

def convertWWPrice(wwPrice):
	logging.info('convertWWPrice')
	return Price(id=wwPrice.getId(), description=wwPrice.getDescription(), pricePerUnit=convertWWPricePerUnit(wwPrice.getPricePerUnit()), unitId=wwPrice.getUnitId(), unitDescription=wwPrice.getDescription())

def convertWWPrices(wwPrices):
    logging.info('convertWWPrices')
    prices = {}
    if wwPrices != None:
	    for index in wwPrices:
	        price = convertWWPrice(wwPrices[index])
	        prices[index] = price
    else:
		print "Prices empty"
    return prices

def convertWWService(wwService):
    logging.info('convertWWService')
    return Service(id=wwService.getId(), name=wwService.getName(), description=wwService.getDescription(), serviceType=wwService.getServiceType(), prices=convertWWPrices(wwService.getPrices()))

def convertWWServiceDetails(wwServiceDetails):
	logging.info('convertWWServiceDetails')
	return ServiceDetails(serviceId=wwServiceDetails.getServiceDetails(), serviceDescription=wwServiceDetails.getServiceDescription())

def convertWWServiceDeliveryToken(wwServiceDeliveryToken):
    logging.info('convertWWServiceDeliveryToken')
    return ServiceDeliveryToken(key=wwServiceDeliveryToken.getKey(), issued=wwServiceDeliveryToken.getIssued(), expiry=wwServiceDeliveryToken.getExpiry(), refundOnExpiry=wwServiceDeliveryToken.getRefundOnExpiry(), signature=wwServiceDeliveryToken.getSignature())

def convertWWServiceMesage(wwServiceMessage):
	logging.info('convertWWServiceMessage')
	return ServiceMessage(deviceDescription=wwServiceMessage.getDeviceDescription(), hostname=wwServiceMessage.getHostname(), portNumber=wwServiceMessage.getServiceMessage(), serverId=wwServiceMessage.getServerId(), urlPrefix=wwServiceMessage.getUrlPrefix(), scheme=wwServiceMessage.getScheme(), deviceName=wwServiceMessage.getDeviceName(),)

def convertWWTotalPriceResponse(wwTotalPriceResponse):
	logging.info('convertWWTotalPriceResponse')
	return TotalPriceResponse(serverId=wwTotalPriceResponse.getServerId(), clientId=wwTotalPriceResponse.getClientId(), priceId=wwTotalPriceResponse.getPriceId(), unitsToSupply=wwTotalPriceResponse.getUnitsToSupply(), totalPrice=wwTotalPriceResponse.getTotalPrice(), paymentReferenceId=wwTotalPriceResponse.getPaymentReferenceId(), merchantClientKey=wwTotalPriceResponse.getMerchantClientKey())

def convertHCECard(hceCard):
	logging.info('convertHCECard')
	wwHceCard = WWTypes.WWHCECard()
	wwHceCard.setFirstName(hceCard.firstName)
	wwHceCard.setLastName(hceCard.lastName)
	wwHceCard.setExpMonth(hceCard.expMonth)
	wwHceCard.setExpYear(hceCard.expYear)
	wwHceCard.setCardNumber(hceCard.cardNumber)
	wwHceCard.setType(hceCard.type)
	wwHceCard.setCvc(hceCard.cvc)
	return wwHceCard

def convertDevice(device):
	logging.info('convertDevice')
	wwDevice = WWTypes.WWDevice()
	wwDevice.setUid(device.uid)
	wwDevice.setName(device.name)
	wwDevice.setDescription(device.description)
	wwDevice.setServices(device.services)
	wwDevice.setIpv4Address(device.ipv4Address)
	wwDevice.setCurrencyCode(device.currencyCode)
	return wwDevice

def convertPaymentResponse(paymentResponse):
    logging.info('convertpaymentResponse')
    wwPaymentResponse = WWTypes.WWPaymentResponse()
    wwPaymentResponse.setServerId(paymentResponse.serverId)
    wwPaymentResponse.setClientId(paymentResponse.clientId)
    wwPaymentResponse.setTotalPaid(paymentResponse.totalPaid)
    wwPaymentResponse.setServiceDeliveryToken(paymentResponse.serviceDeliveryToken)
    return wwPaymentResponse


def convertServicePrices(servicePrices):
	logging.info('convertServicePrices')
	wwServicePrices = []
	for price in servicePrices:
		wwServicePrices.append(convertPrice(price))
	return wwServicePrices

def convertPrice(price):
	logging.info('convertPrice')
	wwPrice = WWTypes.WWPrice()
	wwPrice.setId(price.id)
	wwPrice.setDescription(price.description)
	wwPrice.setPricePerUnit(price.pricePerUnit)
	wwPrice.setUnitId(price.unitId)
	wwPrice.setDescription(price.description)
	return wwPrice

def convertPricePerUnit(pricePerUnit):
	logging.info('convertPricePerUnit')
	wwPricePerUnit = WWTypes.WWPricePerUnit()
	wwPricePerUnit.setAmount(pricePerUnit.getAmount())
	wwPricePerUnit.setCurrencyCode(pricePerUnit.getCurrencyCode())
	return wwPricePerUnit

def convertService(service):
	logging.info('convertService')
	wwService = WWTypes.WWService()
	wwService.setId(service.serverId)
	wwService.setDescription(service.setServiceDescription)
	return wwService

def convertServiceDeliveryToken(serviceDeliveryToken):
    logging.info('convertserviceDeliveryToken')
    wwServiceDeliveryToken = WWTypes.WWServiceDeliveryToken()
    wwServiceDeliveryToken.setKey(serviceDeliveryToken.key)
    wwServiceDeliveryToken.setIssued(serviceDeliveryToken.issued)
    wwServiceDeliveryToken.setExpiry(serviceDeliveryToken.expiry)
    wwServiceDeliveryToken.setRefundOnExpiry(serviceDeliveryToken.refundOnExpiry)
    wwServiceDeliveryToken.setSignature(serviceDeliveryToken.signature)
    return wwServiceDeliveryToken

def convertServiceDetailList(serviceDetailsList):
	logging.info('convertServiceDetailsList')
	wwServiceDetailsList = []
	for serviceDetails in serviceDetailsList:
		wwServiceDetailsList.append(convertServiceDetails(serviceDetails))
	return wwServiceDetailsList

def convertServiceDetails(serviceDetails):
	logging.info('convertServiceDetails')
	wwServiceDetails = WWTypes.WWServiceDetails()
	wwServiceDetails.setServiceId(serviceDetails.serviceId)
	wwServiceDetails.setServiceDescription(serviceDetails.serviceDescription)
	return wwServiceDetails


def convertServiceMessage(serviceMessage):
    logging.info('convertServiceMessage')
    wwServiceMessage = WWTypes.WWServiceMessage()
    wwServiceMessage.setDeviceName(serviceMessage.deviceName)
    wwServiceMessage.setDeviceDescription(serviceMessage.deviceDescription)
    wwServiceMessage.setHostname(serviceMessage.hostname)
    wwServiceMessage.setPortNumber(serviceMessage.portNumber)
    wwServiceMessage.setServerId(serviceMessage.serverId)
    wwServiceMessage.setUrlPrefix(serviceMessage.urlPrefix)
    wwServiceMessage.setScheme('http://')
    wwServiceMessage.setServiceTypes(serviceMessage.serviceTypes)
    return wwServiceMessage

def convertServiceMessages(serviceMessages):
	logging.info('convertServiceMessages')
	wwServiceMessages = []
	for svcMsg in serviceMessages:
		wwServiceMsg = convertServiceMessage(svcMsg)
		wwServiceMessages.append(wwServiceMsg)
	return wwServiceMessages

def convertTotalPriceResponse(totalPriceResponse):
	logging.info('convertTotalPriceResponse')
	wwTotalPriceResponse = WWTypes.WWTotalPriceResponse()
	wwTotalPriceResponse.setServerId(totalPriceResponse.serverId)
	wwTotalPriceResponse.setClientId(totalPriceResponse.clientId)
	wwTotalPriceResponse.setPriceId(totalPriceResponse.priceId)
	wwTotalPriceResponse.setUnitsToSupply(totalPriceResponse.unitsToSupply)
	wwTotalPriceResponse.setTotalPrice(totalPriceResponse.totalPrice)
	wwTotalPriceResponse.setPaymentReferenceId(totalPriceResponse.paymentReferenceId)
	wwTotalPriceResponse.setMerchantClientKey(totalPriceResponse.merchantClientKey)
	return wwTotalPriceResponse

def convertPaymentResponse(paymentResponse):
	logging.info('convertPaymentResponse')
	wwPaymentResponse = WWTypes.WWPaymentResponse()
	wwPaymentResponse.setServerId(paymentResponse.serverId)
	wwPaymentResponse.setClientId(paymentResponse.clientId)
	wwPaymentResponse.setTotalPaid(paymentResponse.totalPaid)
	wwPaymentResponse.setServiceDeliveryToken(convertServiceDeliveryToken(paymentResponse.serviceDeliveryToken))
	return wwPaymentResponse
