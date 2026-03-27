# Sezione degli import 
import time

# Classe per il controllo della modalita clock
class ClockModeController:
    def __init__(self, motore, clock_config):
        self.motore = motore
        self.config = clock_config
        self.tenda_aperta = True  
        
    def aggiorna(self):
        ora_corrente = time.localtime()[3]
        minuto_corrente = time.localtime()[4]
        ora_minuto = (ora_corrente, minuto_corrente)

        if self.motore is None:
            print("Motore non assegnato!")
            return

        apertura = self.config.apertura
        chiusura = self.config.chiusura

        def dentro_intervallo(orario, inizio, fine):
            if inizio < fine:
                return inizio <= orario < fine
            else:
                
                return orario >= inizio or orario < fine

        if dentro_intervallo(ora_minuto, apertura, chiusura):
            if not self.tenda_aperta:
                orario_str = "{:02d}:{:02d}".format(*apertura)
                self.motore.open(msg=f"Buongiorno! Sono passate le {orario_str}. Apertura tenda...")
                self.tenda_aperta = True
        else:
            if self.tenda_aperta:
                orario_str = "{:02d}:{:02d}".format(*chiusura)
                self.motore.close(msg=f"Sono passate le {orario_str}. Chiusura tenda...")
                self.tenda_aperta = False

