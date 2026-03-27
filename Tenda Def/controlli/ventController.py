# Classe per il controllo della ventola
class ventController:
    def __init__(self, mqtt_client, relee: ReleeVentola, topic_comando, topic_stato=None):
        self.client = mqtt_client
        self.relee = relee
        self.topic_comando = topic_comando
        self.topic_stato = topic_stato
        self.client.set_callback(self.mqtt_callback)
        self.client.subscribe(self.topic_comando)

    def mqtt_callback(self, topic, msg):
        comando = msg.decode().lower()

        if comando == "on":
            self.relee.accendi()
            if self.topic_stato:
                self.client.publish(self.topic_stato, b"accesa")
        elif comando == "off":
            self.relee.spegni()
            if self.topic_stato:
                self.client.publish(self.topic_stato, b"spenta")

    def loop(self):
        self.client.check_msg()
        
        
        
