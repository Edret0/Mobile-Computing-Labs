import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Set the logging level to DEBUG
logging.getLogger('AWSIoTPythonSDK.core').setLevel(logging.DEBUG)

class MQTTClient:
    def __init__(self, client_id, endpoint, root_ca_path, private_key_path, certificate_path):
        self.client_id = client_id
        self.endpoint = endpoint
        self.root_ca_path = root_ca_path
        self.private_key_path = private_key_path
        self.certificate_path = certificate_path
        self.mqtt_client = None
    
    def configure_client(self):
        self.mqtt_client = AWSIoTMQTTClient(self.client_id)
        self.mqtt_client.configureEndpoint(self.endpoint, 8883)
        self.mqtt_client.configureCredentials(self.root_ca_path, self.private_key_path, self.certificate_path)
    
    def connect(self):
        self.mqtt_client.connect()
    
    def disconnect(self):
        self.mqtt_client.disconnect()
    
    def subscribe(self, topic, callback):
        self.mqtt_client.subscribe(topic, 1, callback)
    
    def publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload, 1)
        
        

# Example usage for device named 'thing_0'
if __name__ == "__main__":
    # Initialize MQTT client
    thing_0_client = MQTTClient(
        client_id="thing_test",
        endpoint="a3rejv7izsyui2-ats.iot.us-east-1.amazonaws.com",
        root_ca_path="C:/Users/Deylis/Documents/Test/AmazonRootCA1.pem",
        private_key_path="C:/Users/Deylis/Documents/Test/db17596a1b11b9fc5f303fe4669fb7fe488bc2af065ef5bbfd451a21fceaabdd-private.pem.key",
        certificate_path="C:/Users/Deylis/Documents/Test/db17596a1b11b9fc5f303fe4669fb7fe488bc2af065ef5bbfd451a21fceaabdd-certificate.pem.crt"
    )

    # Configure MQTT client
    thing_0_client.configure_client()

    # Connect to AWS IoT Core
    thing_0_client.connect()

    # Subscribe to a topic
    def on_message_received(client, userdata, message):
        print("Received message on topic '{}': {}".format(message.topic, message.payload.decode()))

    thing_0_client.subscribe("myTopic", on_message_received)

    # Publish a message
    thing_0_client.publish("myTopic", "Hello from thing_0!")

    # Disconnect from AWS IoT Core
    thing_0_client.disconnect()
