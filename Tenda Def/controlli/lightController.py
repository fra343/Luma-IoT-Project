# Sezione degli import 
import ujson

# Classe per il controllo della modalità luce
class LightController:
    def __init__(self, tsl_sensor, stepmotor, soglia_alta=800.0, soglia_bassa=600.0):
        self.sensor = tsl_sensor
        self.motor = stepmotor
        self.soglia_alta = soglia_alta
        self.soglia_bassa = soglia_bassa
        self.tenda_aperta = self.motor.tenda_aperta
        self.modalita_automatica = True 
        

    def aggiorna(self):
        if not self.modalita_automatica:
            return 

        try:
            lux = self.sensor.read_lux()
            print("Luce rilevata:", lux)

            if lux > self.soglia_alta and self.tenda_aperta:
                self.chiudi_tenda()
            elif lux < self.soglia_bassa and not self.tenda_aperta:
                self.apri_tenda()
              
        except Exception as e:
            print("Errore durante la lettura o controllo tenda:", e)

    def apri_tenda(self):
        self.motor.open()
        self.tenda_aperta = True

    def chiudi_tenda(self):
        self.motor.close()
        self.tenda_aperta = False

    def ricevi_comando_mqtt(self, msg):
        try:
            comando = msg.decode('utf-8').lower()
            if comando == "manuale_apri":
                print("MQTT: comando manuale_apri ricevuto")
                self.modalita_automatica = False
                self.apri_tenda()
            elif comando == "manuale_chiudi":
                print("MQTT: comando manuale_chiudi ricevuto")
                self.modalita_automatica = False
                self.chiudi_tenda()
            elif comando == "auto":
                print("MQTT: modalità automatica riattivata")
                self.modalita_automatica = True
            else:
                print("MQTT: comando sconosciuto:", comando)
        except Exception as e:
            print("Errore nel parsing comando MQTT:", e)


