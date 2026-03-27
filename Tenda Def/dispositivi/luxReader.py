# Sezione degli import 
import time

class TSL2561:
    TSL2561_ADDR = 0x39  # Indirizzo I2C corretto
    CMD = 0x80
    CTRL = 0x00
    TIMING = 0x01
    CHAN0_LOW = 0x0C
    CHAN1_LOW = 0x0E

    def __init__(self, i2c, addr=TSL2561_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.enable()

    def enable(self):
        self.i2c.writeto_mem(self.addr, self.CMD | self.CTRL, b'\x03')  # Power ON
        self.i2c.writeto_mem(self.addr, self.CMD | self.TIMING, b'\x02')  # 402ms integration time
        time.sleep_ms(500)
        
    def read_word(self, reg):
        data = self.i2c.readfrom_mem(self.addr, self.CMD | reg, 2)
        return data[1] << 8 | data[0]

    def read_lux(self):
        ch0 = self.read_word(self.CHAN0_LOW)
        ch1 = self.read_word(self.CHAN1_LOW)
        if ch0 == 0:
            return 0

        ratio = ch1 / ch0
        if ratio <= 0.5:
            lux = 0.0304 * ch0 - 0.062 * ch0 * (ratio ** 1.4)
        elif ratio <= 0.61:
            lux = 0.0224 * ch0 - 0.031 * ch1
        elif ratio <= 0.80:
            lux = 0.0128 * ch0 - 0.0153 * ch1
        elif ratio <= 1.30:
            lux = 0.00146 * ch0 - 0.00112 * ch1
        else:
            lux = 0
        return max(lux, 0)


