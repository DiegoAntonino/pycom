import machine
from network import WLAN
from conf import conf
import gc


def wifi_connect():
    """
    Connect to the WiFi network based on the configuration. Fails silently if there is no configuration.
    """
    network_config = conf.known_nets
    connected = False
    if not network_config:
        print("wifi - There is not Network Configuration")
        return connected
    try:
        wlan = WLAN(mode=WLAN.STA)

        print("Scanning wifi nets")
        available_nets = wlan.scan()
        nets = frozenset([e.ssid for e in available_nets])

        if list(network_config.keys())[0] in nets:
            sec = [e.sec for e in available_nets if e.ssid == list(network_config.keys())[0]][0]
            wlan.connect(list(network_config.keys())[0], (sec, list(network_config.values())[0]['pwd']), timeout=10000)
            while not wlan.isconnected():
                machine.idle()
            print("Connected to {} with IP address: {}".format(wlan.ssid(), wlan.ifconfig()[0]))
            connected = True
        else:
            print("Could not find network: {}".format(list(network_config.keys())[0]))

    except Exception as e:
        print("Failed to connect to any known network. \nnet_to_use: {}\nError: {}".format(list(network_config.keys())[0], e))

    finally:
        gc.collect()
        return connected
