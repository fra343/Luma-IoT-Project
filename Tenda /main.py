from machine import Pin, I2C
import ujson, utime, time
from dispositivi.led import Led
from dispositivi.stepMotor import StepMotor
from dispositivi.clock import Clock
from dispositivi.releeVentola import ReleeVentola
from dispositivi.luxReader import TSL2561
from dispositivi.dhtSensor import DHTSensor
from controlli.ventController import ventController
from controlli.clockModeController import ClockModeController
from controlli.dhtModeController import DHTController
from controlli.lightController import LightController
from controlli.MQTTCallbackHandler import MQTTCallbackHandler
from comunicazione.networkUtils import WiFi
from umqtt.simple import MQTTClient

CLOCK_MODE = False
TEMPHUM_MODE = False
LIGTH_MODE = False
VENTOLA_MODE = False
MANUAL_MODE = False
last_dht_check = 0

#CONFIGURAZIONE
WIFI_SSID = ''
WIFI_PASSWORD = ''
MQTT_BROKER = ''
MQTT_TOPICS = {
    b'casa/ventola': 'ventola',
    b'tenda/comando' : 'comando', 
    b'Porta': 'porta',
    b'tempHumMode': 'soglia_umidita', 
    b'minTemp': 'soglia_apertura', 
    b'maxTemp': 'soglia_chiusura', 
    b'casa/richiestaDati':'dati', 
    b'clockMode': 'on', 
    b'open': 'openTime',
    b'close': 'closeTime', 
    b'lightMode': 'on', 
    b'casa/chart/light': 'lux', 
    b'tenda/step': 'step' 
}


#CALLBACK MQTT
def mqtt_callback(topic, msg):
    global CLOCK_MODE, TEMPHUM_MODE, LIGTH_MODE, VENTOLA_MODE, MANUAL_MODE,  last_dht_check
    topic = topic.decode("utf-8")
    msg_str = msg.decode("utf-8").strip()
    now = utime.ticks_ms()
    

    if topic == 'open':
        clock_controller.set_orario_apertura(msg_str)
    elif topic == 'close':
        clock_controller.set_orario_chiusura(msg_str)
    elif topic == 'clockMode':
        CLOCK_MODE = True
        TEMPHUM_MODE = False
        LIGTH_MODE = False
        VENTOLA_MODE = False
        print('ClockMode ON')
        clock_mode.aggiorna()
    elif topic == 'lightMode':
        LIGTH_MODE = True
        CLOCK_MODE = False
        TEMPHUM_MODE = False
        VENTOLA_MODE = False
        print("LightMode ON")
        light_controller.aggiorna()
    elif topic == 'minTemp':
        dht_controller.set_soglia_freddo(msg_str)
    elif topic == 'maxTemp':
        dht_controller.set_soglia_caldo(msg_str)
    elif topic == 'tempHumMode' and utime.ticks_diff(now, last_dht_check) > 5000:
        TEMPHUM_MODE = True
        CLOCK_MODE = False
        LIGTH_MODE = False
        VENTOLA_MODE = False
        print("TempHumMode ON")
        last_dht_check = now
        dht_controller.aggiorna()
        if topic == "casa/richiestaDati":
            dht_controller.misura()
            print("Temperatura:", dht_controller.temp)
            print("Umidità:", dht_controller.hum)        # Controlla dispositivi
            dht_controller.controlla_tenda()
            # Pubblica valori sui topic per i grafici
            client.publish("casa/richiestaDati", dht_controller.temp, dht_controller.hum)
    elif topic == 'casa/ventola':
        VENTOLA_MODE = True
        TEMPHUM_MODE = False
        CLOCK_MODE = False
        LIGTH_MODE = False
        if msg_str.lower() == 'on':
            ventola.accendi()
            print("Ventola accesa da MQTT")
        elif msg_str.lower() == 'off':
            ventola.spegni()
            print("Ventola spenta da MQTT")
        else:
            print("Comando ventola non riconosciuto:", msg_str)
    elif topic == 'tenda/comando' :
        MANUAL_MODE = True
        VENTOLA_MODE = False
        TEMPHUM_MODE = False
        CLOCK_MODE = False
        LIGTH_MODE = False
        current_steps = motore.get_steps() 
        mqtt_client.publish(b'tenda/step', str(current_steps))
        if msg_str.lower() == 'apri' :
            motore.open()
            print('tenda aperta mqtt')
        else:
            motore.close()
            print('tenda chiusa mqtt')
        
            
#CONNETTI A WIFI E BROKER MQTT
mqtt_client = WiFi.setup_mqtt('esp32_main_2', MQTT_BROKER, MQTT_TOPICS.keys(), mqtt_callback, WIFI_SSID, WIFI_PASSWORD)

#INIZIALIZZA DISPOSITIVI
motore = StepMotor(32, 33, 25, 27, mqtt_client=mqtt_client)
ventola = ReleeVentola(5)
led_in = Led(2)
clock_controller = Clock(motore)
clock_mode = ClockModeController(motore, clock_controller)
dht_controller = DHTController(pin_sensore=17, motore=motore)

i2c = I2C(0, scl=Pin(23), sda=Pin(22))  
sensor_luce = TSL2561(i2c)
light_controller = LightController(sensor_luce, motore)

orario_apertura = (0, 0)
orario_chiusura = (23, 59)
last_check = utime.ticks_ms()

#LOOP PRINCIPALE
while True:
    try:
        mqtt_client.check_msg()  
    except Exception as e:
        print("Errore MQTT:", e)

    # Ogni 3 secondi, aggiorna stato e pubblica valori
    if utime.ticks_diff(utime.ticks_ms(), last_check) > 3000:
        last_check = utime.ticks_ms()
        try:
            temp, hum = dht_controller.temp, dht_controller.hum
            mqtt_client.publish(b"casa/richiestaDati", f"{temp}|{hum}")
        except Exception as e:
            print("Errore pubblicazione MQTT:", e)

        if CLOCK_MODE:
            clock_mode.aggiorna()
        elif LIGTH_MODE:
            light_controller.aggiorna()
            try:
                lux = sensor_luce.read_lux()
                mqtt_client.publish(b"casa/chart/light", str(lux))
            except Exception as e:
                print("Errore lettura lux:", e)
        elif TEMPHUM_MODE:
            dht_controller.aggiorna()
        elif VENTOLA_MODE:
            pass 

