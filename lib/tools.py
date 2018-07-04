import pycom
import machine
import urequests as requests
import conf
import utime


def datetime_toIso(time):
    return "{}-{}-{}T{}:{}:{}".format(time[0], time[1], time[2], time[3], time[4], time[5])


def led_error():
    if pycom.heartbeat():
        pycom.heartbeat(False)
    pycom.rgbled(0x190000)
#    return True
#    machine.reset()


def send_values(body, send_failed=False):
    failed = False
    URL = conf.ST_IP_PORT
    headers = {"Content-Type": "application/json"}

    try:
        r = requests.request("POST", URL, body, headers)
    except Exception as e:
        print("{} - error: 'tools-send_values' - message: Exception - {}".format(datetime_toIso(utime.localtime()), e))
        led_error()
        failed = True
    else:
        if r.get('status_code') == 202 or r.get('status_code') == 200:
            if send_failed:
                pycom.heartbeat(True)
                utime.sleep(1)
                pycom.heartbeat(False)
        else:
            print("{} - error: '{}' - message: {}".format(datetime_toIso(utime.localtime()), r.get("status_code"), r.get("reason")))
            led_error()
            failed = True
    finally:
        return failed
