#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import machine
import math
import network
import os
import time
import utime
import gc
from lora_functions import Lora
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import LoRa
import socket
import ubinascii
import pycom

time.sleep(.5)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("0.us.pool.ntp.org")

py = Pytrack()
l76 = L76GNSS(py, timeout=30)
lora = Lora()
lora.connect()
# lora.send('Hello World')
while (True):
    coord = l76.coordinates()
    # print(str(coord))
    lora.send(str(coord))
    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))