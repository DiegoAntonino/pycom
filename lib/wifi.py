import machine
from network import WLAN
import conf

class WIFI():
    """docstring for WIFI."""
    def __init__(self):
        known_nets = conf.known_nets

        wlan = WLAN(mode=WLAN.STA)
        print("Scanning for known wifi nets")
        available_nets = wlan.scan()
        nets = frozenset([e.ssid for e in available_nets])

        known_nets_names = frozenset([key for key in known_nets])
        net_to_use = list(nets & known_nets_names)

        try:
            net_to_use = net_to_use[0]
            pwd = known_nets.get(net_to_use).get('pwd')
            sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
            wlan.connect(net_to_use, (sec, pwd), timeout=10000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print("Connected to '"+net_to_use+"' with IP address: " + wlan.ifconfig()[0])

        except Exception as e:
            print("Failed to connect to any known network. Error: {}".format(e))
