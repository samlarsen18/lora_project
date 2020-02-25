from network import LoRa
import socket
import time
import ubinascii
import pycom

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED002B40D')
app_key = ubinascii.unhexlify('F55D18E92BEB28624993A1CCD35D86AE')

# const char *appEui = "70B3D57ED002B40D";
# const char *appKey = "F55D18E92BEB28624993A1CCD35D86AE";

pycom.heartbeat(False)  # Turn off the default blinking so you know the program is running
pycom.rgbled(0x050000)  # Make the LED red

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)


# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

pycom.rgbled(0x000500)  # Make the LED green


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)



# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)