import socket
import struct
from network import LoRa
import pycom


def logBadPacket(errMsg='Bad packet received, ignoring', filename='BadPacketLog.txt'):
    print(errMsg)
    try:
        f = open(filename, 'a+')
        f.write(errMsg)
        f.close()
    except():
        print('Could not log error')


# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formatted string for string
_LORA_PKG_FORMAT = "!BB%ds"
# A basic ack package, B: 1 byte for the deviceId, B: 1 byte for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"
_LORA_PKG_SIZE = 512
_LORA_PREAMBLE_SIZE = 2
_LORA_PKG_MSG_LENGTH = _LORA_PKG_SIZE - _LORA_PREAMBLE_SIZE
_LORA_ACK_CODE_OK = 200
_LORA_ACK_SIZE = 3
_LORA_ACK_PREAMBLE_SIZE = 2
_LORA_ACK_MSG_LENGTH = _LORA_ACK_SIZE - _LORA_ACK_PREAMBLE_SIZE

pycom.heartbeat(False)  # Turn off the default blinking so you know the program is running
pycom.rgbled(0x050000)  # Make the LED red

# Open a LoRa Socket, use rx_iq to avoid listening to our own messages
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.US915)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

pycom.rgbled(0x050500)  # Make the LED green

while (True):
    recv_pkg = lora_sock.recv(_LORA_PKG_SIZE)
    if (len(recv_pkg) > _LORA_PREAMBLE_SIZE):
        recv_pkg_len = recv_pkg[1]

        if (recv_pkg_len <= _LORA_PKG_MSG_LENGTH
                and recv_pkg_len == (len(recv_pkg) - _LORA_PREAMBLE_SIZE)):

            try:
                device_id, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len,
                                                        recv_pkg)
                # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
                print('Device: %d - Pkg:  %s' % (device_id, msg))
                ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id,
                                      _LORA_ACK_MSG_LENGTH, _LORA_ACK_CODE_OK)
                lora_sock.send(ack_pkg)
            except():
                logBadPacket()
        else:
            logBadPacket()
