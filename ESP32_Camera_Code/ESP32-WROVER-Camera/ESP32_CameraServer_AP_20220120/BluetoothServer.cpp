#include "BluetoothServer.h"
#include <ArduinoJson.h>
/*
Most of the code except the creation of listening for client response is coppied from the BLE_notfiy example.
Which is an external dependancy which is from Neil Kolban, which as the current version of 
Arduino IDE it is provided and you won't have to download it yourself.
*/
BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID_RX "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define CHARACTERISTIC_UUID_TX "beb5483f-36e1-4688-b7f5-ea07361b26a8"

void MyServerCallbacks::onConnect(BLEServer* pServer) {
    deviceConnected = true;
    Serial.println("Client connected");
}

void MyServerCallbacks::onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
    Serial.println("Client disconnected");
}

void MyCharacteristicCallbacks::onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();
    Serial.print("Received value: ");
    Serial.println(value.c_str());
    if(strcmp(value.c_str(),"f") == 0) {
      JsonDocument doc;
      Serial.println("forward");
      doc["N"] = 102;
      doc["D1"] = 1;
      doc["D2"] = 200;
      serializeJsonPretty(doc, Serial2);
      delay(500);
      doc.clear();
      doc["N"] = 100;
      serializeJsonPretty(doc, Serial2);
    }
    else if(strcmp(value.c_str(),"b") == 0) {
      JsonDocument doc;
      Serial.println("backward");
      doc["N"] = 102;
      doc["D1"] = 2;
      doc["D2"] = 200;
      serializeJsonPretty(doc, Serial2);
      delay(500);
      doc.clear();
      doc["N"] = 100;
      serializeJsonPretty(doc, Serial2);
    }
    else if(strcmp(value.c_str(),"l") == 0) {
      JsonDocument doc;
      Serial.println("left");
      doc["N"] = 102;
      doc["D1"] = 3;
      doc["D2"] = 200;
      serializeJsonPretty(doc, Serial2);
      delay(250);
      doc.clear();
      doc["N"] = 100;
      serializeJsonPretty(doc, Serial2);
    }
    else if(strcmp(value.c_str(),"r") == 0) {
      JsonDocument doc;
      Serial.println("right");
      doc["N"] = 102;
      doc["D1"] = 4;
      doc["D2"] = 200;
      serializeJsonPretty(doc, Serial2);
      delay(250);
      doc.clear();
      doc["N"] = 100;
      serializeJsonPretty(doc, Serial2);
    }
    
}

void setupBluetooth() {
    BLEDevice::init("ESP32");
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
    BLEService *pService = pServer->createService(SERVICE_UUID);
    pCharacteristic = pService->createCharacteristic(
                          CHARACTERISTIC_UUID_TX,
                          BLECharacteristic::PROPERTY_READ   |
                          BLECharacteristic::PROPERTY_WRITE  |
                          BLECharacteristic::PROPERTY_NOTIFY |
                          BLECharacteristic::PROPERTY_INDICATE
                        );
    pCharacteristic->addDescriptor(new BLE2902());
    BLECharacteristic *pCharacteristic = pService->createCharacteristic(
      CHARACTERISTIC_UUID_RX,
      BLECharacteristic::PROPERTY_WRITE
    );
    pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());
    pService->start();
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(false);
    pAdvertising->setMinPreferred(0x0);
    BLEDevice::startAdvertising();
    Serial.println("Waiting a client connection to notify...");
}

void loopBluetooth() {
    if (deviceConnected) {
        pCharacteristic->setValue((uint8_t*)&value, 4);
        pCharacteristic->notify();
        value++;
        delay(3);
    }
    if (!deviceConnected && oldDeviceConnected) {
        delay(500);
        pServer->startAdvertising();
        Serial.println("start advertising");
        oldDeviceConnected = deviceConnected;
    }
    if (deviceConnected && !oldDeviceConnected) {
        oldDeviceConnected = deviceConnected;
    }
}
