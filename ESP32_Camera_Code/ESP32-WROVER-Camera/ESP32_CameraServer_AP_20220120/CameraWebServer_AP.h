/*
 * @Descripttion: 
 * @version: 
 * @Author: Elegoo
 * @Date: 2020-06-04 11:42:27
 * @LastEditors: Changhua
 * @LastEditTime: 2020-07-23 14:21:48
 */

#ifndef _CameraWebServer_AP_H
#define _CameraWebServer_AP_H
#include "esp_camera.h"
#include <WiFi.h>
#include <esp_wifi.h>
#include <Arduino.h>
#define MAX_ADDRESSES 10
class CameraWebServer_AP
{

public:
  void CameraWebServer_AP_Init(void);
  void CameraWebServer_AP_Get_Devices();
  void FilterByIp();
  String wifi_name;
  WiFiServer server{80};

private:
  // const char *ssid = "ESP32_CAM";
  // const char *password = "elegoo2020";
  char *ssid = "ELEGOO-";
  //char *password = "elegoo2020";
  char *password = "FooBarBizzBuzz@8080";
  String allowedMACAddresses[MAX_ADDRESSES] = {"ba:9d:d1:c1:3:93"};
};

#endif
