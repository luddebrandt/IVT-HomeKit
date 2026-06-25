import os
import can
import time
import datetime
import sqlite3

#sudo nano /boot/config.txt
#dtparam=spi=on
#dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
#sudo reboot

#Convert idx from rego1000-v3.9.0-variables.txt
#hex((idx << 14) | 201342944)
#hex((0x030B << 14) | 201342944)
#hex((0x030B << 14) | 67125216)

#Convert message.data
def convertM(message):
    val = int(message.hex(), 16)
    if (val & (1 << (16 - 1))) != 0:
        val = val - (1 << 16)
    return float(val)/10  

class readIVT:

    def __init__(self):

        try:
            os.system('sudo ifconfig can0 down')
            os.system('sudo ip link set can0 type can bitrate 125000')
            os.system('sudo ifconfig can0 up')
        except:
            pass

        self.filters = [{"can_id": 0xCC2FFE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCC4FFE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCC73FE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCCF7FE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCDA3FE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCDCBFE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCBC7FE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCBFFFE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xCFC7FE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xC6D7FE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xC6DFFE0, "can_mask": 0xFFFFFFF, "extended": True},
                        {"can_id": 0xC56BFE0, "can_mask": 0xFFFFFFF, "extended": True},]

        self.GT1 = 0
        self.GT2 = 0
        self.GT3 = 0
        self.GT6 = 0
        self.GT8 = 0
        self.GT9 = 0
        self.GT10 = 0
        self.GT11 = 0
        self.VK1 = 0
        self.VV1 = 0
        self.VV1o = 0
        self.CS = 0

        conn = sqlite3.connect('IVT.db', timeout=10)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ivt(Time, GT1, GT2, GT3, GT6, GT8, GT9, GT10, GT11, VK1, VV1, VV1o, CS)')
        conn.commit()
        conn.close()

    def read(self):

        for i in range(1,13):   
            try:
                with can.Bus(channel = 'can0', interface = 'socketcan', bitrate=125000, can_filters=self.filters) as bus:
        
                    if i==1:
                        #GT1_TEMP Heat Carrier 1
                        messageSend = can.Message(arbitration_id=0x4C2FFE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCC2FFE0':
                                #print('Radiator forward: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT1 = convertM(message.data)
                                break
                            else:
                                self.GT1 = 10              
                    if i==2:
                        #GT2_TEMP Outdoor
                        messageSend = can.Message(arbitration_id=0x4C4FFE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCC4FFE0':
                                #print('Outdoor: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C') 
                                self.GT2 = convertM(message.data)
                                break
                    if i==3:
                        #GT3_TEMP Warm water
                        messageSend = can.Message(arbitration_id=0x4C73FE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCC73FE0':
                                #print('Warm water: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT3 = convertM(message.data)
                                break
                    if i==4:
                        #GT6_TEMP Hot gas
                        messageSend = can.Message(arbitration_id=0x4CF7FE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCCF7FE0':
                                #print('Hot gas: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT6 = convertM(message.data)
                                break
                    if i==5:
                        #GT8_TEMP Heat fluid out
                        messageSend = can.Message(arbitration_id=0x4DA3FE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCDA3FE0':
                                #print('Heat fluid out: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT8 = convertM(message.data)
                                break
                    if i==6:
                        #GT9_TEMP Heat fluid in
                        messageSend = can.Message(arbitration_id=0x4DCBFE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCDCBFE0':
                                #print('Heat fluid in: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT9 = convertM(message.data)
                                break
                    if i==7:
                        #GT10_TEMP Cold fluid in
                        messageSend = can.Message(arbitration_id=0x4BC7FE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCBC7FE0':
                                #print('Cold fluid in: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT10 = convertM(message.data)
                                break
                    if i==8:
                        #GT11_TEMP Cold fluid out
                        messageSend = can.Message(arbitration_id=0x4BFFFE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCBFFFE0':
                                #print('Cold fluid out: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.GT11 = convertM(message.data)
                                break
                    if i==9:
                        #VK1 setpoint
                        messageSend = can.Message(arbitration_id=0x4FC7FE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xCFC7FE0':
                                #print('Setpoint radiator forward: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.VK1 = convertM(message.data)
                                break
                    if i==10:
                        #DHW_CALCULATED_SETPOINT_TEMP Varmvatten1 setpoint
                        messageSend = can.Message(arbitration_id=0x46D7FE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xC6D7FE0':
                                #print('Setpoint warm water: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.VV1 = convertM(message.data)
                                break
                    if i==11:
                        #DHW_CALCULATED_SETPOINT_TEMP_OFFSET Varmvatten1 offset
                        messageSend = can.Message(arbitration_id=0x46DFFE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xC6DFFE0':
                                #print('Setpoint warm water offset: ' + str(convertM(message.data)) + ' ' + chr(176) + 'C')
                                self.VV1o = convertM(message.data)
                                break
                    if i==12:
                        #COMPRESSOR_STATE
                        messageSend = can.Message(arbitration_id=0x456BFE0, is_remote_frame=True, is_extended_id=True, dlc=0)
                        bus.send(messageSend)
                        for j in range(1,10):
                            message = bus.recv(timeout=10)
                            if '0x{:X}'.format(message.arbitration_id) == '0xC56BFE0':
                                #print('Compressor: ' + str(int(message.data.hex(), 16)))
                                self.CS = int(message.data.hex(), 16)
                                break
                    
                    #print(messageSend)
                    #print(message)
                    
                    bus.shutdown()
                    
                    time.sleep(0.5)
            except:
                pass

        try:
            self.saveSQL()
        except:
            pass

    def saveSQL(self):
        conn = sqlite3.connect('IVT.db', timeout=10)
        #conn = sqlite3.connect('IVT.db', timeout=10)
        cur = conn.cursor()
        now = datetime.datetime.now()
        values = (now.strftime('%Y-%m-%d %H:%M:%S'), self.GT1, self.GT2, self.GT3, self.GT6, self.GT8, self.GT9, self.GT10, self.GT11, self.VK1, self.VV1, self.VV1o, self.CS)
        cur.execute("INSERT INTO ivt('Time', 'GT1', 'GT2', 'GT3', 'GT6', 'GT8', 'GT9', 'GT10', 'GT11', 'VK1', 'VV1', 'VV1o', 'CS') VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", values)
        conn.commit()
        #for row in cur.execute('SELECT * FROM ivt'):
            #print(row)
        conn.close()

    #def stop(self):
        #self.bus.shutdown()
        #os.system('sudo ifconfig can0 down')