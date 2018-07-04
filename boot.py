import machine
import pycom
import utime
from lib import wifi, tools

if machine.reset_cause() != machine.SOFT_RESET:
    wifi.WIFI()
    #initialize DateTime
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep(5)
    print("DateTime(UTC): {}".format(tools.datetime_to_iso(rtc.now())))
    pycom.heartbeat(False)
