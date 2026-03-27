from time import sleep

#Classe per la gestione della callback MQTT
class MQTTCallbackHandler:
    def __init__(self, servo, oled):
        self.servo = servo
        self.oled = oled

    def handle(self, topic, msg):
        topic = topic.decode()
        comando = msg.decode().strip().lower()
        print("MQTT:", topic, comando)

        if topic == 'Porta':
            if comando == "apri":
                self.servo.open()
            elif comando == "chiudi":
                self.servo.close()
            else:
                print("From MQTT: error occurred!")

        elif topic == 'casa/ventola':
            if comando == 'on':
                self.oled.show_text("Vent mode ON", 15, 30)
                sleep(2)
                self.oled.clear()
            elif comando == 'off':
                self.oled.show_text("Vent mode OFF", 10, 30)
                sleep(2)
                self.oled.clear()

        elif topic == 'tempHumMode':
            if comando == 'on':
                self.oled.show_text("Temp mode ON", 15, 30)
                sleep(2)
                self.oled.clear()
            else:
                self.oled.show_text("Temp mode OFF", 20, 30)
                sleep(2)
                self.oled.clear()

        elif topic == 'tenda/comando':
            if comando == 'apri':
                self.oled.show_text('LUMA opening...', 6, 30)
                sleep(2)
                self.oled.clear()
            elif comando == 'chiudi':
                self.oled.show_text('LUMA closing...', 6, 30)
                sleep(2)
                self.oled.clear()

        elif topic == 'clockMode':
            if comando == 'on':
                self.oled.show_text("CK mode ON", 20, 30)
                sleep(2)
                self.oled.clear()
            else:
                self.oled.show_text("CK mode OFF", 20, 30)
                sleep(2)
                self.oled.clear()

        elif topic == 'lightMode':
            if comando == 'on':
                self.oled.show_text("Light mode ON", 15, 30)
                sleep(2)
                self.oled.clear()
            else:
                self.oled.show_text("Light mode OFF", 20, 30)
                sleep(2)
                self.oled.clear()