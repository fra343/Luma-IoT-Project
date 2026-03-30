from machine import Pin
import time
import ujson
import os

class StepMotor:
    def __init__(self, in1, in2, in3, in4, delay_ms=2, mqtt_client=None):
        self.pins = [Pin(in1, Pin.OUT), Pin(in2, Pin.OUT), Pin(in3, Pin.OUT), Pin(in4, Pin.OUT)]
        self.delay_ms = delay_ms
        self.seq = [[1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
        self.step_count = 0
        self.mqtt_client = mqtt_client
        self.state_file = "tenda_state.json"
        self.tenda_aperta = self._leggi_stato_tenda()
        print("Stato tenda al boot:", "Aperta" if self.tenda_aperta else "Chiusa")

    def get_steps(self):
        return self.step_count

    def step(self, direction=1):
        seq = self.seq if direction == 1 else list(reversed(self.seq))
        for i in seq:
            for j in range(4):
                self.pins[j].value(i[j])
            time.sleep_ms(self.delay_ms)
        self.step_count += direction
        self.publish_step_count()

    def rotate(self, steps, direction=1):
        for _ in range(steps):
            self.step(direction)

    def open(self, steps=1350, msg="Apertura tenda..."):
        if self.tenda_aperta is False:
            print(msg)
            self.rotate(steps, direction=-1)
            self.tenda_aperta = True
            self._salva_stato_tenda(True)
            print("Tenda aperta!")

    def close(self, steps=1350, msg="Chiusura tenda..."):
        if self.tenda_aperta is True:
            print(msg)
            self.rotate(steps, direction=1)
            self.tenda_aperta = False
            self._salva_stato_tenda(False)
            print("Tenda chiusa!")

    def publish_step_count(self):
        if self.mqtt_client:
            try:
                self.mqtt_client.publish(b"tenda/step", str(self.step_count))
            except Exception as e:
                print("Errore publish step:", e)

    def _salva_stato_tenda(self, aperta):
        try:
            with open(self.state_file, "w") as f:
                ujson.dump({"tenda_aperta": aperta}, f)
        except Exception as e:
            print("Errore salvataggio stato tenda:", e)

    def _leggi_stato_tenda(self):
        try:
            if self.state_file in os.listdir():
                with open(self.state_file, "r") as f:
                    stato = ujson.load(f)
                    return stato.get("tenda_aperta", False)
        except Exception as e:
            print("Errore lettura stato tenda:", e)
        return False  # default = tenda chiusa
