from machine import I2C

class TSL2561:
    """Initialice i2c with tsl2561"""
    def __init__(self, addr=0x39):
        self.i2c = I2C(0, I2C.MASTER, baudrate=100000)
        self.addr = addr

        #Power ON
        self.i2c.writeto_mem(self.addr, 0x80, 0x03)
        #Set Gain 1x and integration time to 402ms
        self.i2c.writeto_mem(self.addr, 0x81, 0x02)

    def get_lux(self):
        data = self.i2c.readfrom_mem(self.addr, 0x8C, 4)  #read 4 addresses in once...

        ch0 = ((data[1] << 8) + data[0])
        ch1 = ((data[3] << 8) + data[2])

        return self.get_lumi(ch0, ch1)

    @staticmethod
    def get_lumi(ch0, ch1):
        """
        Read the luminosity in units of Lux.
        """
        lux = 0.0
        if ch0 != 0:
            c = ch1 / ch0
            if c > 0:
                if c <= 0.5:
                    lux = 0.0304 * ch0 - 0.062 * ch0 * pow(c, 1.4)
                elif c <= 0.61:
                    lux = 0.0224 * ch0 - 0.031 * ch1
                elif c <= 0.8:
                    lux = 0.0128 * ch0 - 0.0153 * ch1
                elif c <= 1.3:
                    lux = 0.00146 * ch0 - 0.00112 * ch1
                else:
                    lux = 0.0

        return float(lux * 100.0)
