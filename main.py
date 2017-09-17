# main.py -- put your code here!
import pycom
import time
import machine
import sys
import tools

from tsl2561 import TSL2561
import urequests as requests

light_sensor = TSL2561()
URL = "https://run-east.att.io/b8c5703c726bc/b59e0c890712/fc61e0e361d821e/in/flow/test"
#URL = "http://192.168.1.252:39500"
headers = {"Content-Type" : "application/json"}
pycom.heartbeat(False)
error = False

print("Starting Main loop")
while True:
    ch0, ch1, lux  = light_sensor.get_lux()
    body = {
    'lux': lux,
    'ir_light': ch1,
    'total_light': ch0,
    'visible_light': ch0 - ch1
    }

    try:
        r = requests.request("POST", URL, body, headers)
    except ValueError as e:
        print("{} - ValueError: {}".format(tools.datetime_toIso(time.localtime()), e) )
        error = tools.led_error()
    except NotImplementedError as e:
        print("{} - NotImplementedError: {}".format(tools.datetime_toIso(time.localtime()), e) )
        error = tools.led_error()
    except Exception as e:
        print("{} - Exception: {}".format(tools.datetime_toIso(time.localtime()), e) )
        error = tools.led_error()
    else:
        if r.get('status_code') == 202 or r.get('status_code') == 200:
            if error:
                error = False
                pycom.heartbeat(True)
                time.sleep(1)
                pycom.heartbeat(False)

        else:
            print("error: {} - message: {}".format(r.get("status_code"), r.get("reason")))
            error = tools.led_error()
    finally:
        time.sleep(300)
