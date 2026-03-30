from machine import Pin, PWM
from time import sleep

#Classe del servo motore
class Servo:
    def __init__(self, pin, freq=50, min_duty=25, max_duty=125):
        self.pwm = PWM(Pin(pin), freq=freq)
        self.min_duty = min_duty
        self.max_duty = max_duty

    def angle(self, angolo):
        angolo = max(0, min(180, angolo))
        duty = int((self.min_duty + (angolo / 180) * (self.max_duty - self.min_duty)))
        self.pwm.duty(duty)

    def open(self):
        print("Door opening...")
        self.angle(180)
        sleep(1)

    def close(self):
        print("Door closing...")
        self.angle(90)
        sleep(1)