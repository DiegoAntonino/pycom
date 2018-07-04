# main.py -- put your code here!
import pycom
import time
import machine
from tsl2561 import TSL2561
import tools

light_sensor = TSL2561()
retry_num = 5
retry_min_msec = 200
error = False

time.sleep(1)
print("Starting Main loop")
while True:
    lux  = light_sensor.get_lux()
    body = {
        'lux': float(lux)
    }
    #print(tools.datetime_toIso(time.localtime()),"-", body)

    send_completed, error = tools.send_values(body, error)
    retry = 0
    while retry < retry_num and not send_completed:
        time.sleep(pow(2, retry)*retry_min_msec/1000)
        #Debug
        #print("{} - retry: {}".format(tools.datetime_toIso(time.localtime()), retry) )
        send_completed, error = tools.send_values(body, error)
        retry+=1

    if retry >= retry_num and not send_completed:
        print ("Tried: {} times and it coudn't send values. Waiting 5 min".format(retry))

    if lux > 200 and lux < 1000 :
        time.sleep(5)
    else:
        time.sleep(300)
