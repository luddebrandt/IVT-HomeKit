import signal
import time

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap.const import CATEGORY_SENSOR, CATEGORY_SWITCH, CATEGORY_LIGHTBULB, CATEGORY_ALARM_SYSTEM, CATEGORY_THERMOSTAT, CATEGORY_HEATER

time.sleep(3)

#Connect to IVT
readIVT = readIVT()
#readIVT.read()

UpdateIntervalIVT = 120

#Radiator forward
class Thermostat1(Accessory):

    category = CATEGORY_THERMOSTAT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('Thermostat')
        self.char_temp1 = serv_temp.configure_char('CurrentTemperature')
        self.char_temp2 = serv_temp.configure_char('TargetTemperature', setter_callback=self.set_TargetTemperature)
        self.char_temp3 = serv_temp.configure_char('CurrentHeatingCoolingState', value=1)
        self.char_temp4 = serv_temp.configure_char('TargetHeatingCoolingState', value=3, setter_callback=self.set_TargetHeatingCoolingState)
        self.char_temp5 = serv_temp.configure_char('TemperatureDisplayUnits', value=0)
        
    def set_TargetTemperature(self, value):
        temp2 = readIVT.VK1
        self.char_temp2.set_value(temp2)

    def set_TargetHeatingCoolingState(self, value):
        self.char_temp4.set_value(3)

    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        #Update values
        readIVT.read()
        temp1 = readIVT.GT1
        self.char_temp1.set_value(temp1)
        temp2 = readIVT.VK1
        self.char_temp2.set_value(temp2)
        stateC = readIVT.CS
        if stateC == 1:
            self.char_temp3.set_value(1)
        else:
            self.char_temp3.set_value(0)
#Warm water
class Thermostat3(Accessory):

    category = CATEGORY_THERMOSTAT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('Thermostat')
        self.char_temp1 = serv_temp.configure_char('CurrentTemperature')
        self.char_temp2 = serv_temp.configure_char('TargetTemperature', setter_callback=self.set_TargetTemperature)
        self.char_temp3 = serv_temp.configure_char('CurrentHeatingCoolingState', value=1)
        self.char_temp4 = serv_temp.configure_char('TargetHeatingCoolingState', value=3, setter_callback=self.set_TargetHeatingCoolingState)
        self.char_temp5 = serv_temp.configure_char('TemperatureDisplayUnits', value=0)
        
    def set_TargetTemperature(self, value):
        temp2 = readIVT.VV1 + readIVT.VV1o
        self.char_temp2.set_value(temp2)

    def set_TargetHeatingCoolingState(self, value):
        self.char_temp4.set_value(3)

    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp1 = readIVT.GT3
        self.char_temp1.set_value(temp1)
        temp2 = readIVT.VV1 + readIVT.VV1o
        self.char_temp2.set_value(temp2)
        stateC = readIVT.CS
        if stateC == 2:
            self.char_temp3.set_value(1)
        else:
            self.char_temp3.set_value(0)
#Värmepump
class Thermostat4(Accessory):

    category = CATEGORY_THERMOSTAT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('Thermostat')
        self.char_temp1 = serv_temp.configure_char('CurrentTemperature')
        self.char_temp2 = serv_temp.configure_char('TargetTemperature', setter_callback=self.set_TargetTemperature)
        self.char_temp3 = serv_temp.configure_char('CurrentHeatingCoolingState', value=1)
        self.char_temp4 = serv_temp.configure_char('TargetHeatingCoolingState', value=1, setter_callback=self.set_TargetHeatingCoolingState)
        self.char_temp5 = serv_temp.configure_char('TemperatureDisplayUnits', value=0)
        
    def set_TargetTemperature(self, value):
        temp2 = readIVT.GT8
        self.char_temp2.set_value(temp2)

    def set_TargetHeatingCoolingState(self, value):
        self.char_temp4.set_value(1)

    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp1 = readIVT.GT9
        self.char_temp1.set_value(temp1)
        temp2 = readIVT.GT8
        self.char_temp2.set_value(temp2)
        stateC = readIVT.CS
        if stateC == 1 or stateC == 2:
            self.char_temp3.set_value(1)
        else:
            self.char_temp3.set_value(0)
'''
#Hot gas
class HeaterCooler6(Accessory):

    category = CATEGORY_HEATER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('HeaterCooler')
        self.char_temp4 = serv_temp.configure_char('CurrentTemperature')
        self.char_temp2 = serv_temp.configure_char('CurrentHeaterCoolerState', value=2)
        self.char_temp1 = serv_temp.configure_char('Active', value=1, setter_callback=self.set_ActiveState)
        self.char_temp3 = serv_temp.configure_char('TargetHeaterCoolerState', value=1, setter_callback=self.set_TargetHeaterCoolerState)

    def set_ActiveState(self, value):
        self.char_temp1.set_value(1)

    def set_TargetHeaterCoolerState(self, value):
        self.char_temp3.set_value(1)
         
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT6
        self.char_temp4.set_value(temp)
'''
#Radiator forward
class TemperatureSensor1(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT1
        self.char_temp.set_value(temp)
#Outdoor
class TemperatureSensor2(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT2
        self.char_temp.set_value(temp)
#Warm water
class TemperatureSensor3(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT3
        self.char_temp.set_value(temp)
#Hot gas
class TemperatureSensor6(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT6
        self.char_temp.set_value(temp)
#Heat fluid out
class TemperatureSensor8(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT8
        self.char_temp.set_value(temp)
#Heat fluid in
class TemperatureSensor9(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT9
        self.char_temp.set_value(temp)
#Cold fluid in
class TemperatureSensor10(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT10
        self.char_temp.set_value(temp)
#Cold fluid out
class TemperatureSensor11(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.GT11
        self.char_temp.set_value(temp)
#VK1 setpoint
class TemperatureSensor12(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')
        
    @Accessory.run_at_interval(UpdateIntervalIVT)
    async def run(self):
        temp = readIVT.VK1
        self.char_temp.set_value(temp)

'''
#Restart Raspberry Pi
class ShutdownSwitch(Accessory):

    category = CATEGORY_SWITCH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_switch = self.add_preload_service('Switch')
        self.char_on = serv_switch.configure_char('On', setter_callback=self.execute_shutdown)

    def execute_shutdown(self, value):
        #os.system("sudo shutdown -h now")
        os.system("sudo shutdown -r now")
'''

def get_bridge(driver):
    bridge = Bridge(driver, 'Raspberry Pi')

    bridge.add_accessory(Thermostat1(driver, 'Golvvärme'))
    bridge.add_accessory(Thermostat3(driver, 'Varmvatten'))
    bridge.add_accessory(Thermostat4(driver, 'Värmepump'))
    #bridge.add_accessory(HeaterCooler6(driver, 'Kompressor'))
    bridge.add_accessory(TemperatureSensor1(driver, 'Golvvärme'))
    bridge.add_accessory(TemperatureSensor2(driver, 'Utomhus'))
    bridge.add_accessory(TemperatureSensor3(driver, 'Varmvatten'))
    bridge.add_accessory(TemperatureSensor6(driver, 'Kompressor'))
    bridge.add_accessory(TemperatureSensor8(driver, 'VP ut'))
    bridge.add_accessory(TemperatureSensor9(driver, 'VP retur'))
    bridge.add_accessory(TemperatureSensor10(driver, 'Brine retur'))
    bridge.add_accessory(TemperatureSensor11(driver, 'Brine ut'))
    bridge.add_accessory(TemperatureSensor12(driver, 'Börvärde'))
    
    #bridge.add_accessory(ShutdownSwitch(driver, "Restart Raspberry Pi"))
    
    return bridge

driver = AccessoryDriver(port=51826)

driver.add_accessory(accessory=get_bridge(driver))

signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()