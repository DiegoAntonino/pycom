import pycom
import utime
import machine
from tsl2561 import TSL2561
import tools

light_sensor = TSL2561()
retry_num = 5
retry_min_msec = 200

utime.sleep(1)
print("Starting Main loop")
while True:
    lux = light_sensor.get_lux()
    body = {
        'lux': lux
    }

    send_failed = tools.send_values(body)
    retry = 0
    while retry < retry_num and send_failed:
        utime.sleep(pow(2, retry)*retry_min_msec/1000)
        send_failed = tools.send_values(body, send_failed)
        retry += 1

    if retry >= retry_num and send_failed:
        print("Tried: {} times and it coudn't send values.".format(retry))

    if 200 < lux < 1000:
        utime.sleep(5)
    else:
        utime.sleep(300)
