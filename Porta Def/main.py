from machine import Pin
from time import sleep
from dispositivi.led import Led
from dispositivi.servoMotor import Servo
from dispositivi.oled import OledDisplayManager,logo
from dispositivi.ultrasonic import SensoreUltrasuoni
from dispositivi.tastierino import MainController
from controlli.MQTTCallbackHandler import MQTTCallbackHandler
from comunicazione.networkUtils import WiFi
import ujson

#Sezione di configurazione della connessione
WIFI_SSID = ''
WIFI_PASSWORD = ''
MQTT_BROKER = ''
MQTT_TOPICS = {
    'casa/led': 'led',
    'Porta': 'porta',
    'casa/ventola':'ventola',
    'tempHumMode':'temp_mode',
    'tenda/comando': 'tenda',
    'clockMode' : 'clock',
    'lightMode' : 'light'
}

def mqtt_callback(topic, msg):
    callback_handler.handle(topic, msg)

#Sezione di inizializzazione dei componenti che operano sulla ESP32
righe_pins = [2, 0, 4, 16]
colonne_pins = [17, 5, 18, 19]
servo_pin = 26
servo = Servo(26)
led_out = Led (23)
oled = OledDisplayManager(scl_pin=22, sda_pin=21)
ultrasonic = SensoreUltrasuoni(33,32)
main_controller = MainController(righe_pins, colonne_pins, servo_pin, oled)
callback_handler = MQTTCallbackHandler(servo,oled)

#Funzioni di connessione
WiFi.connect_wifi(WIFI_SSID, WIFI_PASSWORD,oled)
mqtt_client = WiFi.setup_mqtt('esp32_main', MQTT_BROKER, MQTT_TOPICS.keys(), mqtt_callback,oled)

password_inserita = False
#Funzionamento
while True:
    mqtt_client.check_msg()                        

    distanza = ultrasonic.misura_distanza()
    ultrasonic.aggiorna(led_out,oled,distanza)
    
    if distanza is not None:
        if distanza < 10 and not password_inserita:
            sleep(1)
            oled.clear()
            result = main_controller.run()
            password_inserita = result
        elif distanza > 30:
            password_inserita = False
    sleep(1)



