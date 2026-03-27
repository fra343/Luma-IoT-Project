import network
from time import sleep
import time  # serve per time.sleep()
from umqtt.simple import MQTTClient
# Rimuovo OledDisplayManager se non usi il display in questo file
# from dispositivi.oled import OledDisplayManager

class WiFi:
    
    def __init__(self, oled):
        self.oled = oled

    @staticmethod
    def connect_wifi(ssid, password, oled):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            oled.show_text('Connecting WiFi', 5, 30)
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                sleep(1)
        oled.show_text('Connected!', 15, 30)

    @staticmethod
    def setup_wifi(ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        print("Connessione WiFi...")
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)

        print("\nConnesso! IP:", wlan.ifconfig()[0])
        return wlan

    @staticmethod
    def setup_mqtt(client_id, broker, topics, callback, ssid, password):
        WiFi.setup_wifi(ssid, password)
        client = MQTTClient(client_id, broker)
        client.set_callback(callback)
        client.connect()

        for topic in topics:
            client.subscribe(topic)
            print(f"Iscritto a {topic.decode()}")

        return client


