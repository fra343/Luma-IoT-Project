# Sezione degli import
from machine import Pin,PWM

# Classe per la gestione del led
class Led:
    def __init__(self, pin, freq = 5000):
        self.pwm = PWM(Pin(pin, Pin.OUT), freq)
        self.pwm.duty(0)

    def freq(self, freq):
        self.pwm.freq(freq)

    def duty(self, duty):
        self.pwm.duty(duty)

    def on(self):
        self.duty(1023)

    def off(self):
        self.duty(0)
