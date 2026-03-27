# Sezione degli import
import dht
from machine import Pin
from time import sleep

# Ckasse per il controllo del sensore di temperatura ed umitidtà
class DHTController:
    def __init__(self, pin_sensore, motore, t_hot=25, t_cool=24, h_high=60, h_low=40):
        self.dht = dht.DHT22(Pin(pin_sensore))
        self.motore = motore
        self.t_hot = t_hot        
        self.t_cool = t_cool      
        self.h_high = h_high      
        self.h_low = h_low        
        self.temp = None
        self.hum = None

    def misura(self):
        self.dht.measure()
        self.temp = self.dht.temperature()
        self.hum = self.dht.humidity()

    def controlla_tenda(self):
        if self.temp > self.t_hot:
            self.motore.close()
        elif self.temp < self.t_cool:
            self.motore.open()

    def aggiorna(self):
        try:
            self.misura()
            print("Temp:", self.temp, "°C | Hum:", self.hum, "%")
            self.controlla_tenda()
        except OSError as e:
            print("Errore nel sensore DHT:", e) 

    def set_soglia_caldo(self, valore):
        self.t_hot = float(valore)
        print("Soglia temperatura alta aggiornata a:", self.t_hot)

    def set_soglia_freddo(self, valore):
        self.t_cool = float(valore)
        print("Soglia temperatura bassa aggiornata a:", self.t_cool)


