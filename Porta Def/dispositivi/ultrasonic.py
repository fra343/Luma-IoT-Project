from machine import Pin, time_pulse_us
import time 
from dispositivi.oled import OledDisplayManager, logo
from dispositivi.led import Led

#Classe del sensore ad ultrasuoni
class SensoreUltrasuoni:
    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
    
    def misura_distanza(self):
        self.trig.off()
        time.sleep_us(2)
        self.trig.on()
        time.sleep_us(10)
        self.trig.off()

        durata = time_pulse_us(self.echo, 1, 30000)
        if durata < 0:
            return None
        distanza = (durata / 2) / 29.1
        return distanza
    
    def aggiorna(self,led_out,oled,distanza):
        if distanza is not None:
            if distanza < 20:
                led_out.on()
                if distanza < 10:
                    oled.show_image(logo)
                    time.sleep(5)
                    oled.clear()
                else:
                    oled.clear()
            else:
                led_out.off()
        else:
            led_out.off()

