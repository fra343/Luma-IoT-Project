# Sezione degli import
from machine import Pin

# Classe per la gestione del rele che gestisce la ventola
class ReleeVentola:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(1)  # Spento all'inizio

    def accendi(self):
        self.pin.value(0)

    def spegni(self):
        self.pin.value(1)

    def is_attiva(self):
        return self.pin.value() == 0
