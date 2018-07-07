import utime
from lib import tools, tsl2561

retry_num = 5
retry_min_msec = 200

try:
    #light_sensor = tsl2561.TSL2561()
    print("waiting 10 seconds to stop the main")
    utime.sleep(10)
    pass
except Exception as e:
    print("Failed to initialize Light Sensor. Error: {}".format(e))
    tools.led_error()
else:
    print("Starting Main loop")
    while True:
        lux = 0
        try:
            #lux = light_sensor.get_lux()

            ####### workaround until i get the sensor
            time = utime.localtime()
            if 0 <= time[3] <= 11:  # from 20hs to 7am hs EST. localtime gives UTC
                lux = 0
            else:
                lux = 1000
            ###################################
        except Exception as e:
            print("Failed to get luminosity. Error: {}".format(e))
            tools.led_error()
        else:
            body = {'lux': lux}
            send_failed = tools.send_values(body)
            retry = 0
            while retry < retry_num and send_failed:
                utime.sleep(pow(2, retry)*retry_min_msec/1000)
                send_failed = tools.send_values(body, send_failed)
                retry += 1

            if retry >= retry_num and send_failed:
                print("Tried: {} times and it couldn't send values.".format(retry))
        finally:
            #if 200 < lux < 1000:
            #    utime.sleep(5)
            #else:
            #    utime.sleep(300)

            ####### workaround until i get the sensor
            utime.sleep(300)
            ###################################
