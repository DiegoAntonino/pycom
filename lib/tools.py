import pycom
import utime
from lib import urequests as requests
from conf import conf
import gc

def datetime_to_iso(time):
    return "{}-{}-{}T{}:{}:{}".format(time[0], time[1], time[2], time[3], time[4], time[5])

def led_error(color=0x190000):
    pycom.rgbled(color)

def send_values(body, send_failed=False):
    failed = False
    URL = conf.ST_IP_PORT
    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post(URL, json=body, headers=headers)
    except Exception as e:
        print("{} - error: 'tools-send_values' - message: Exception - {}".format(datetime_to_iso(utime.localtime()), e))
        #led_error()
        failed = True
    else:
        if r.status_code == 202 or r.status_code == 200:
            pycom.rgbled(0)
        else:
            print("{} - error: '{}' - message: {}".format(datetime_to_iso(utime.localtime()), r.get("status_code"), r.get("reason")))
            #led_error()
            failed = True

    gc.collect()
    return failed
