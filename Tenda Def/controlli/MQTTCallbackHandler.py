import utime

class MQTTCallbackHandler:
    def __init__(self, motore, ventola, clock_controller, clock_mode, dht_controller, light_controller, mqtt_client):
        self.motore = motore
        self.ventola = ventola
        self.clock_controller = clock_controller
        self.clock_mode = clock_mode
        self.dht_controller = dht_controller
        self.light_controller = light_controller
        self.mqtt_client = mqtt_client

        self.CLOCK_MODE = False
        self.TEMPHUM_MODE = False
        self.LIGHT_MODE = False
        self.VENTOLA_MODE = False
        self.MANUAL_MODE = False
        self.last_dht_check = 0

    def mqtt_callback(self, topic, msg):
        topic = topic.decode("utf-8")
        msg_str = msg.decode("utf-8").strip()
        now = utime.ticks_ms()

        if topic == 'open':
            self.clock_controller.set_orario_apertura(msg_str)
        elif topic == 'close':
            self.clock_controller.set_orario_chiusura(msg_str)
        elif topic == 'clockMode':
            self.reset_modes()
            self.CLOCK_MODE = True
            print('ClockMode ON')
            self.clock_mode.aggiorna()
        elif topic == 'lightMode':
            self.reset_modes()
            self.LIGHT_MODE = True
            print("LightMode ON")
            self.light_controller.aggiorna()
        elif topic == 'minTemp':
            self.dht_controller.set_soglia_freddo(msg_str)
        elif topic == 'maxTemp':
            self.dht_controller.set_soglia_caldo(msg_str)
        elif topic == 'tempHumMode' and utime.ticks_diff(now, self.last_dht_check) > 5000:
            self.reset_modes()
            self.TEMPHUM_MODE = True
            print("TempHumMode ON")
            self.last_dht_check = now
            self.dht_controller.aggiorna()
        elif topic == 'casa/richiestaDati':
            self.dht_controller.misura()
            print("Temperatura:", self.dht_controller.temp)
            print("Umidità:", self.dht_controller.hum)
            self.dht_controller.controlla_tenda()
            self.mqtt_client.publish(b"casa/richiestaDati", f"{self.dht_controller.temp}|{self.dht_controller.hum}")
        elif topic == 'casa/ventola':
            self.reset_modes()
            self.VENTOLA_MODE = True
            if msg_str.lower() == 'on':
                self.ventola.accendi()
                print("Ventola accesa da MQTT")
            elif msg_str.lower() == 'off':
                self.ventola.spegni()
                print("Ventola spenta da MQTT")
            else:
                print("Comando ventola non riconosciuto:", msg_str)
        elif topic == 'tenda/comando':
            self.reset_modes()
            self.MANUAL_MODE = True
            if msg_str.lower() == 'apri':
                self.motore.open()
                print('Tenda aperta via MQTT')
            else:
                self.motore.close()
                print('Tenda chiusa via MQTT')
            current_steps = self.motore.get_steps()
            self.mqtt_client.publish(b'tenda/step', str(current_steps))

    def reset_modes(self):
        print("Disattivo modalità")
        self.CLOCK_MODE = False
        self.TEMPHUM_MODE = False
        self.LIGHT_MODE = False
        self.VENTOLA_MODE = False
        self.MANUAL_MODE = False
