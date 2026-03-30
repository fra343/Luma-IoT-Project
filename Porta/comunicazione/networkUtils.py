import network
from time import sleep
from umqtt.simple import MQTTClient
from dispositivi.oled import OledDisplayManager

#Classe WiFi per gestire la connessione alla rete e il setup MQTT
class WiFi:
    
    def __init__(self,oled):
        self.oled = oled

    @staticmethod
    def connect_wifi(ssid, password,oled):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            oled.show_text('Connecting WiFi',5,30)
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                sleep(1)
        oled.show_text('Connected!',27,30)

    @staticmethod
    def setup_mqtt(client_id, broker, topics, callback,oled):
        client = MQTTClient(client_id, broker)
        client.set_callback(callback)
        client.connect()
        for t in topics:
            client.subscribe(t)
        oled.show_text('MQTT Connected!',5,30)
        sleep(3)
        oled.clear()
        return client
