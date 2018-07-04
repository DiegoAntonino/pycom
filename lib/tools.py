import pycom
import machine
import urequests as requests

def datetime_toIso(time):
    return "{}-{}-{}T{}:{}:{}".format(time[0], time[1], time[2], time[3], time[4], time[5])

def led_error():
    if pycom.heartbeat():
        pycom.heartbeat(False)
    pycom.rgbled(0x190000)
    return True
#    machine.reset()

def send_values(body, error):
    answer = False
    #URL = "https://run-east.att.io/b8c5703c726bc/b59e0c890712/fc61e0e361d821e/in/flow/test"
    URL = "http://192.168.2.23:39500"
    headers = {"Content-Type" : "application/json"}

    try:
        r = requests.request("POST", URL, body, headers)
    except Exception as e:
        print("{} - error: 'tools-send_values' - message: Exception - {}".format(tools.datetime_toIso(time.localtime()), e))
        error = tools.led_error()
    else:
        if r.get('status_code') == 202 or r.get('status_code') == 200:
            if error:
                error = False
                pycom.heartbeat(True)
                time.sleep(1)
                pycom.heartbeat(False)
            answer = True
        else:
            print("{} - error: '{}' - message: {}".format(tools.datetime_toIso(time.localtime()), r.get("status_code"), r.get("reason")))
            error = tools.led_error()
    finally:
        return answer, error
