from network import LoRa
import socket
import time
import ubinascii
import pycom
class Lora:
    # Update these!
    APP_KEY = "APP KEY"  # Application key from the things network SAM
    APP_EUI = "APP EUI"  # The EUI for the app SAM
    DEV_EUI = "DEV EUI"
    JOIN_TIMEOUT = 30  # passed to the LoRaWAN join function.
        

    def connect(self):
        # config = config_template()
        pycom.heartbeat(False)
        pycom.rgbled(0xf00000)  # Make the LED red
        print("Connecting to Lora")

        # United States = LoRa.US915
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915, device_class=LoRa.CLASS_A)

        # Setting up channels for sub-band 2
        self.lora.add_channel(index=8, frequency=903900000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=9, frequency=904100000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=10, frequency=904300000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=11, frequency=904500000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=12, frequency=904700000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=13, frequency=904900000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=14, frequency=905100000, dr_min=0, dr_max=3)
        self.lora.add_channel(index=15, frequency=905300000, dr_min=0, dr_max=3)
        # Remove all other channels
        for index in range(0, 7):
            self.lora.remove_channel(index)
        for index in range(16, 72):
            self.lora.remove_channel(index)

        # create an OTAA authentication parameters
        app_eui = ubinascii.unhexlify(self.APP_EUI)
        app_key = ubinascii.unhexlify(self.APP_KEY)
        dev_eui = ubinascii.unhexlify(self.DEV_EUI)
        # join a network using OTAA (Over the Air Activation)
        self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        count = 0 
        while not self.lora.has_joined():
            time.sleep(2.5)
            print('Not yet...'+ str(count))
            count += 1

        pycom.rgbled(0x008000)  # Make the LED green
        print("Joined Lora Network")
        
    def create_socket(self):
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

    def send(self, msg):
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
        s.setblocking(True)
        # msg_bytes = bytearray()
        # msg_bytes = msg.encode()
        s.send(msg.encode())
        s.close()

    def getStatus(self):
        if self.lora.has_joined():
            return 0
        return 1
