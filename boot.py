# boot.py -- run on boot-up
import os
import machine
from wifi import WIFI
import time
import tools

if machine.reset_cause() != machine.SOFT_RESET:
    WIFI()
    #initialize DateTIme
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    time.sleep(5)
    print("DateTime(UTC): {}".format(tools.datetime_toIso(rtc.now())))
