import pycom
import utime
from lib import urequests as requests
from conf import conf


def datetime_to_iso(time):
    return "{}-{}-{}T{}:{}:{}".format(time[0], time[1], time[2], time[3], time[4], time[5])


def led_error(color=0x190000):
    if pycom.heartbeat():
        pycom.heartbeat(False)
    pycom.rgbled(color)


def send_values(body, send_failed=False):
    failed = False
    URL = conf.ST_IP_PORT
    headers = {"Content-Type": "application/json"}

    try:
        r = requests.request("POST", URL, body, headers)
    except Exception as e:
        print("{} - error: 'tools-send_values' - message: Exception - {}".format(datetime_to_iso(utime.localtime()), e))
        led_error()
        failed = True
    else:
        if r.get('status_code') == 202 or r.get('status_code') == 200:
            if send_failed:
                pycom.heartbeat(True)
                utime.sleep(1)
                pycom.heartbeat(False)
        else:
            print("{} - error: '{}' - message: {}".format(datetime_to_iso(utime.localtime()), r.get("status_code"), r.get("reason")))
            led_error()
            failed = True
    finally:
        return failed
