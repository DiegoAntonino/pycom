import gc
import utime
from lib.tools import datetime_to_iso, led_error
from lib import urequests as requests
from conf import conf
import uerrno
import sys


class Smartthings():
    def __init__(self, retry_num=5, retry_sec=1):
        self.retry_num = retry_num
        self.retry_sec = retry_sec
        self.requests = requests

    def notify(self, body):
        try:
            attempts = self.retry_num
            print("{} - Smartthings.notify, Sent body: {}".format(datetime_to_iso(utime.localtime()), body))

            while attempts and self.send_values(body):
                attempts -= 1
                print("{} - Smartthings.notify, Re-try: {} - Body: {}".format(datetime_to_iso(utime.localtime()),
                                                                              (self.retry_num - attempts), body))
                utime.sleep(pow(2, (self.retry_num - attempts)) * self.retry_sec)

            if not attempts:
                print("{} - Smartthings.notify - Tried: {} times and it couldn't send readings. free_memory: {}".format(
                    datetime_to_iso(utime.localtime()), self.retry_num, gc.mem_free()))
                led_error()

        except Exception as e:
            print("{} - Smartthings.notify - Exception: {}".format(datetime_to_iso(utime.localtime()), e))
            sys.print_exception(e)
            led_error()

        finally:
            gc.collect()

    def send_values(self, body):
        failed = True
        headers = {"Content-Type": "application/json"}

        try:
            gc.collect()
            r = self.requests.post(conf.ST_IP_PORT, json=body, headers=headers)
        except OSError as e:
            if e.args[0] == uerrno.EAI_MEMORY:
                print("{} - Smartthings.send_values' - 'OSError.EAI_MEMORY' Exception. Restarting Device".format(datetime_to_iso(utime.localtime())))
                sys.print_exception(e)
                utime.sleep(2)
                #machine.reset()
            else:
                print("{} - Smartthings.send_values' - 'OSError': {}".format(datetime_to_iso(utime.localtime()), e))
                sys.print_exception(e)
        except Exception as e:
            print("{} - Smartthings.send_values' - 'Exception': {}, free_memory: {}".format(datetime_to_iso(utime.localtime()), e, gc.mem_free()))
            sys.print_exception(e)
        else:
            if r.status_code == 202 or r.status_code == 200:
                led_error(0)
                failed = False
            else:
                print("{} - 'Smartthings.send_values' - HTTP_Status_Code: '{}' - HTTP_Reason: {}".format(
                    datetime_to_iso(utime.localtime()), r.get("status_code"), r.get("reason")))
            r.close()
        finally:
            gc.collect()
            return failed
