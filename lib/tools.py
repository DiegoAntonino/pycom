import pycom
import gc


def datetime_to_iso(time, tz=None):
    [year, month, day, hour, minute, seconds] = convert_date_number([time[0], time[1], time[2], time[3], time[4], time[5]])

    if tz:
        gc.collect()
        return "{}-{}-{}T{}:{}:{}{}".format(year, month, day, hour, minute, seconds, tz)
    else:
        gc.collect()
        return "{}-{}-{}T{}:{}:{}".format(year, month, day, hour, minute, seconds)


def convert_date_number(numbers):
    out = []
    for num in numbers:
        if num < 10:
            out.append("0{}".format(num))
        else:
            out.append("{}".format(num))
    gc.collect()
    return out


def led_error(color=0x190000):
    pycom.rgbled(color)
    gc.collect()

