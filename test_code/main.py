from network import LoRa
import socket
import time
import ubinascii
import pycom
# import config_template

class config_template:
    # Update these values! 
    APP_KEY = "APP KEY"  # Application key from the things network SAM
    APP_EUI = "APP EUI"  # The EUI for the app SAM
    DEV_EUI = "DEV EUI"
    JOIN_TIMEOUT = 30  # passed to the LoRaWAN join function.
    
config = config_template()
pycom.rgbled(0x050000)  # Make the LED red


# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915, device_class=LoRa.CLASS_A)

# Setting up channels for sub-band 2
lora.add_channel(index=8, frequency=903900000, dr_min=0, dr_max=3)
lora.add_channel(index=9, frequency=904100000, dr_min=0, dr_max=3)
lora.add_channel(index=10, frequency=904300000, dr_min=0, dr_max=3)
lora.add_channel(index=11, frequency=904500000, dr_min=0, dr_max=3)
lora.add_channel(index=12, frequency=904700000, dr_min=0, dr_max=3)
lora.add_channel(index=13, frequency=904900000, dr_min=0, dr_max=3)
lora.add_channel(index=14, frequency=905100000, dr_min=0, dr_max=3)
lora.add_channel(index=15, frequency=905300000, dr_min=0, dr_max=3)
# Remove all other channels
for index in range(0, 7):
    lora.remove_channel(index)
for index in range(16, 72):
    lora.remove_channel(index)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify(config.APP_EUI)
app_key = ubinascii.unhexlify(config.APP_KEY)
dev_eui = ubinascii.unhexlify(config.DEV_EUI)
# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
count = 0 
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet...'+ str(count))
    count += 1

pycom.rgbled(0x000500)  # Make the LED green

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

while True:
    pycom.rgbled(0x000500)  # Make the LED green
    s.send(bytes([0x01, 0x02, 0x03]))
    time.sleep(.5)
    pycom.rgbled(0x5)  # Make the LED green
    time.sleep(.5)
    # data = s.recv(64)
    # print(data)
