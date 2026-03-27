# Sezione degli import
import dht
from machine import Pin

# Classe per la gestione del sensore di temperatura ed umidità
class DHTSensor:
    def __init__(self, pin_sensore):
        self.dht = dht.DHT22(Pin(pin_sensore))
        self.temp = 0
        self.hum = 0

    def misura(self):
        self.dht.measure()
        self.temp = self.dht.temperature()
        self.hum = self.dht.humidity()
        return self.temp, self.hum
    

