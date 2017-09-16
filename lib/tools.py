import pycom
import machine

def datetime_toIso(time):
    return "{}-{}-{}T{}:{}:{}".format(time[0], time[1], time[2], time[3], time[4], time[5])

def led_error():
    pycom.heartbeat(False)
    pycom.rgbled(0xff0000)
#    machine.reset()
