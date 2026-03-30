# Classe per la gestione del clock

class Clock:
    def __init__(self, apertura="07:00", chiusura="20:00"):
        self.apertura = self._parse_orario(apertura) or (7, 0)
        self.chiusura = self._parse_orario(chiusura) or (20, 0)

    def _parse_orario(self, orario_str):
        """Estrae 'HH:MM' da stringhe tipo '1970-01-01T08:29:00.000Z' oppure direttamente '08:29'."""
        try:
            
            if 'T' in orario_str:
                orario_str = orario_str.split('T')[1][:5]  
            
            parts = orario_str.strip().split(":")
            if len(parts) != 2:
                return None
            
            ora = int(parts[0])
            minuti = int(parts[1])
            ora = (ora + 1) % 24  
            if 0 <= ora < 24 and 0 <= minuti < 60:
                return (ora, minuti)
        except Exception as e:
            pass        
        return None

    def set_orario_apertura(self, orario_str):
        orario = self._parse_orario(orario_str)
        if orario:
            self.apertura = orario
            print(f"Orario apertura impostato a: {self.apertura}")
        else:
            print(f"Formato orario apertura non valido: '{orario_str}', imposto default (7:00)")
            self.apertura = (7, 0)

    def set_orario_chiusura(self, orario_str):
        orario = self._parse_orario(orario_str)
        if orario:
            self.chiusura = orario
            print(f"Orario chiusura impostato a: {self.chiusura}")
        else:
            print(f"Formato orario chiusura non valido: '{orario_str}', imposto default (20:00)")
            self.chiusura = (20, 0)

