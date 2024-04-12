#ifndef BLUETOOTH_SERVER_H
#define BLUETOOTH_SERVER_H

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include "Arduino.h"

class MyServerCallbacks : public BLEServerCallbacks {
public:
    void onConnect(BLEServer* pServer);
    void onDisconnect(BLEServer* pServer);
};

// callback whenever the client writes back to the server.
class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
public:
    void onWrite(BLECharacteristic *pCharacteristic);
};

void setupBluetooth();
void loopBluetooth();

#endif 
