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
extern "C" {
  #include <esp_wifi.h>

}
#include <Arduino.h>
#define TOTAL_BOGON_ADDRESSES 16
#define BLOCKED_ADDRESS_SIZE 10

class CameraWebServer_AP
{

public:
  void CameraWebServer_AP_Init(void);
  void CameraWebServer_AP_Get_Devices();
  bool CameraWebServer_AP_Is_Bogon(uint32_t ip);
  String wifi_name;
  WiFiServer server{80};
private:
  // const char *ssid = "ESP32_CAM";
  // const char *password = "elegoo2020";
  char *ssid = "ELEGOO-";
  //char *password = "elegoo2020";
  char *password = "FooBarBizzBuzz1@";

  // bogon Ipv4 address
  const uint32_t bogonIPRanges[TOTAL_BOGON_ADDRESSES] = {
  0x00000000, // 0.0.0.0/8
  0x0A000000, // 10.0.0.0/8
  0x64400000, // 100.64.0.0/10
  0x7F000000, // 127.0.0.0/8
  0x7F003535, // 127.0.53.53/32
  0xA9FE0000, // 169.254.0.0/16
  0xAC100000, // 172.16.0.0/12
  0xC0000000, // 192.0.0.0/24
  0xC0000200, // 192.0.2.0/24
  0xC0A80000, // 192.168.0.0/16
  0xC6120000, // 198.18.0.0/15
  0xC6336400, // 198.51.100.0/24
  0xCB007100, // 203.0.113.0/24
  0xE0000000, // 224.0.0.0/4
  0xF0000000, // 240.0.0.0/4
  0xFFFFFFFF  // 255.255.255.255/32
  };
  IPAddress blockedAddresses[BLOCKED_ADDRESS_SIZE] = {
        IPAddress(120, 30, 4, 2),
        IPAddress(192, 168, 1, 1),
        IPAddress(10, 0, 0, 1),
        IPAddress(172, 16, 0, 1),
        IPAddress(192, 168, 2, 1),
        IPAddress(192, 168, 3, 1),
        IPAddress(192, 168, 4, 1),
        IPAddress(192, 168, 5, 1),
        IPAddress(192, 168, 6, 1),
        IPAddress(192, 168, 7, 1)
    };
};

#endif
