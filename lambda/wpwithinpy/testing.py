import unittest
import WPWithinWrapperImpl
import WWTypes

class TestWPWithinWrapperImpl(unittest.TestCase):


    def createExampleService(self):
        svc = WWTypes.WWService();
        svc.setName("Car charger")
        svc.setDescription("Can charge your hybrid / electric car")
        svc.setId(1)
        ccPrice = WWTypes.WWPrice()
        ccPrice.setId(1)
        ccPrice.setDescription("Kilowatt-hour")
        ccPrice.setUnitDescription("One kilowatt-hour")
        ccPrice.setUnitId(1)
        ppu = WWTypes.WWPricePerUnit()
        ppu.setAmount(25)
        ppu.setCurrencyCode("GBP")
        ccPrice.setPricePerUnit(ppu)
        prices = {}
        prices[ccPrice.getId()] = ccPrice
        svc.setPrices(prices)
        return svc

     

    # Test consumer requestServices out of order...
    def test_requestService(self):
        #requestServices(self):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            services = wpw.requestServices()
        wpw.stopRPCAgent()
        
    # def test_getDevice():
    #     #getDevice(self):

    # def test_deviceDiscovery():
    #     #deviceDiscovery(self, timeout):

    # def test_initConsumer():
    #     #initConsumer(self, scheme, hostname, port, urlPrefix, serverId, hceCard):



    # def test_startServiceBroadcast():
    #     #startServiceBroadcast(self, timeout):

    # def test_stopServiceBroaccast():
    #     #stopServiceBroadcast(self):

    # def test_getServicePrirces():
    #     #getServicePrices(self, serviceId):


    # def test_selectService():
    #     #selectService(self, serviceId, numberOfUnits, priceId):

    # def test_makePayment():
    #     #makePayment(self, request):


    # def test_beginServiceDelivery():
    #     #beginServiceDelivery(self, serviceId, serviceDeliveryToken, unitsToSupply):


    # def test_endServiceDelivery():
    #     #endServiceDelivery(self, serviceId, serviceDeliveryToken, unitsReceived):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_addServiceNone(self):
        #addService(self, theService):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            wpw.addService(None)       
        wpw.stopRPCAgent()

    # Note that it should run without erring, even if in the wrong order
    def test_addServiceSvcOutOfCorrectOrderWithoutProducer(self):
        #addService(self, theService):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        svc = self.createExampleService()
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            wpw.addService(svc)            
        wpw.stopRPCAgent()

    def test_setup(self):
        #setup(self, deviceName, deviceDescription):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        wpw.setup("Test device Name", "Test device description")
        wpw.stopRPCAgent()

    # What happens if you remove a service that hasn't been added - it shouldn't error
    def test_removeServiceNotAddedWithoutProducer(self):
        #removeService(self, svc):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        svc = self.createExampleService()
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            wpw.removeService(svc)            
        wpw.stopRPCAgent()

    def test_removeServiceThatHasBeenAddedWithoutProducer(self):
        #removeService(self, svc):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        svc = self.createExampleService()
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            wpw.addService(svc)
        with self.assertRaises(WWTypes.WPWithinGeneralException):            
            wpw.removeService(svc)            
        wpw.stopRPCAgent()

    def test_removeServiceThatHasBeenAddedWithInitProducer(self):
        #removeService(self, svc):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        wpw.initProducer(None, None)
        svc = self.createExampleService()
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            wpw.addService(svc)
        with self.assertRaises(WWTypes.WPWithinGeneralException):            
            wpw.removeService(svc)            
        wpw.stopRPCAgent()

    def test_removeServiceThatHasBeenAddedAfterInitProducer(self):
        #removeService(self, svc):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        svc = self.createExampleService()
        wpw.initProducer(None, None)
        with self.assertRaises(WWTypes.WPWithinGeneralException):
            wpw.addService(svc)
        with self.assertRaises(WWTypes.WPWithinGeneralException):            
            wpw.removeService(svc)            
        wpw.stopRPCAgent()

    def test_initProducer(self):
        #initProducer(self, clientKey, serviceKey):
        wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
        #interestingly this doesn't err
        wpw.initProducer(None, None)
        wpw.stopRPCAgent()   

if __name__ == '__main__':
    unittest.main()
