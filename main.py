import _thread
import machine
import pycom
import utime
import gc
import sys

from lib import tools, tsl2561
from network import WLAN

retry_num = 5
retry_min_msec = 200

def read_lux(send_failed=False):
    try:
        light_sensor = tsl2561.TSL2561()
        lux = light_sensor.get_lux()
    except Exception as e:
        #pybytes.send_signal(1, "initialize_lux_sensor_failed")
        tools.led_error()
        return
    #pybytes.send_signal(1, "main_loop_started")

    while True:
        try:
            lux = light_sensor.get_lux()
        except Exception as e:
            print("Failed to get luminosity. Error: {}".format(e))
            tools.led_error(0xFFFF00)
            send_failed = True
            #pybytes.send_signal(1, "get_luminosity_failed")
            break
        else:
            body = {'lux': lux}
            #pybytes.send_signal(0, lux)
            try:
                send_failed = tools.send_values(body, send_failed)
                retry = 0
                while retry < retry_num and send_failed:
                    utime.sleep(pow(2, retry)*retry_min_msec/1000)
                    send_failed = tools.send_values(body, send_failed)
                    retry += 1

                if retry >= retry_num and send_failed:
                    print("Tried: {} times and it couldn't send readings.".format(retry))
                    tools.led_error()
                    #pybytes.send_signal(1, "sent_event_{}_time_failed".format(retry_num))
            except Exception as e:
                print("Error trying to send event to ST: {}".format(e))
        finally:
            if 200 < lux < 400:
                gc.collect()
                utime.sleep(30)
            else:
                gc.collect()
                utime.sleep(300)


def initialize_RTC():
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep(5)
    print("DateTime(UTC): {}".format(tools.datetime_to_iso(rtc.now())))
    pycom.heartbeat(False)
    utime.sleep(1)


#START MAIN PROCESS
try:
    initialize_RTC()
except Exception as e:
    print("Failed to initialize RTC. Error: {}".format(e))
    #pybytes.send_signal(1, "initialize_rtc_failed")
    tools.led_error()

gc.collect()
try:
    print("Starting Main loop")
    _thread.start_new_thread(read_lux, (False,))
    #read_lux()
except Exception as e:
    print(e)
