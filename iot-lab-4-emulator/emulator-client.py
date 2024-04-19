#Script to publish messages via MQTT using AWS IoT

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np
import random


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 0
device_end = 3

#Path to the dataset, modify this
data_path = "C:/Mobile-Computing-Labs/iot-lab-4-emulator/data/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = r"C:/Mobile-Computing-Labs/iot-lab-4-emulator/certificates/{}/cert_thing_{}.pem"
key_formatter = r"C:/Mobile-Computing-Labs/iot-lab-4-emulator/private_certificates/{}/private_thing_{}.key"

class MQTTClient:
    def __init__(self, thing_name, cert, key):
        # For certificate based connection
        self.thing_name = str(thing_name)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.thing_name)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a3rejv7izsyui2-ats.iot.us-east-1.amazonaws.com", 8883)
        self.client.configureCredentials(r"C:/Mobile-Computing-Labs/iot-lab-4-emulator/AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage

        print("Initializing MQTT client for Thing:", self.thing_name)
        try:
            print("Connecting to AWS IoT for Thing:", self.thing_name)
            self.client.connect()
            print("Connected to AWS IoT for Thing:", self.thing_name)
        except Exception as e:
            print("Failed to connect to AWS IoT for Thing:", self.thing_name)
                       
            
    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callbacks
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload):
        #TODO4: fill in this function for your publish
        self.client.subscribeAsync("myTopic", 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("myTopic", Payload, 0, ackCallback=self.customPubackCallback)


print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for i in range(device_st, device_end):
    thing_name = "thing_" + str(i)  # Form the Thing name
    cert_path = certificate_formatter.format(i, i)
    key_path = key_formatter.format(i, i)  
    client = MQTTClient(i, cert_path, key_path)     
    clients.append(client)

while True:
    print("Send now? (s), Disconnect (d)")
    x = input()
    if x == "s":
       for i, c in enumerate(clients):
            #payload = data[i].to_dict(orient='list')  # Convert DataFrame to dictionary
            #print("Payload for device {}: {}".format(i, json.dumps(payload)))
            #c.publish(json.dumps(payload))  # Pass data as payload after converting to JSON
            c.publish(data[i])  # Pass data as payload
       print("Messages sent")
    elif x == "d":
       for c in clients:
           c.client.disconnect()                    
       print("All devices disconnected")
       exit()
    else:
        print("Wrong key pressed")

    time.sleep(3)