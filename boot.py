import machine
import pycom
import utime
from lib import wifi, tools

#  permanently disable the heartbeat LED.
if pycom.heartbeat_on_boot():
    pycom.heartbeat_on_boot(False)
    machine.reset()

if machine.reset_cause() != machine.SOFT_RESET:
    wifi.WIFI()
    #initialize DateTime
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep(5)
    print("DateTime(UTC): {}".format(tools.datetime_to_iso(rtc.now())))
