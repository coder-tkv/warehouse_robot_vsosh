#ifndef bluetooth
#define bluetooth


#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


BluetoothSerial SerialBT;


String receiveRoute() {
  SerialBT.begin("ESP32BT-EGGR");
  Serial.println("The device started, now you can pair it with bluetooth!");

  String check = "";
  String incoming = "";

  while (true) {
    if (SerialBT.available()) {
      check += (char)SerialBT.read();
      if (check.length() > 3) {
        check = check.substring(check.length() - 3);  // последние 3 символа
      }

      if (check == "tkv") {
        // Читаем до символа 'e'
        while (true) {
          if (SerialBT.available()) {
            char c = SerialBT.read();
            incoming += c;
            if (c == 'e') break;
          }
        }
        Serial.println("Received: " + incoming);
        return incoming;
      }
    }
  }
}


void parseRouteString(String incoming, uint8_t coords[], uint8_t &coords_length, uint8_t &start_level) {
  coords_length = 0;
  start_level = 0;

  bool inCoords = false;
  bool inStart  = false;
  String num = "";

  for (int i = 0; i < incoming.length(); i++) {
    char c = incoming.charAt(i);

    // начало списка координат
    if (c == 'p') {
      inCoords = true;
      inStart  = false;
      num = "";
      continue;
    }

    // начало start_level (после координат)
    if (c == 's') {
      // перед переключением не забываем сохранить последнее число координат
      if (inCoords && num.length() > 0) {
        coords[coords_length++] = (uint8_t)num.toInt();
        num = "";
      }
      inCoords = false;
      inStart  = true;
      continue;
    }

    // конец строки
    if (c == 'e') {
      // добиваем хвост того, что не успели сохранить
      if (inCoords && num.length() > 0) {
        coords[coords_length++] = (uint8_t)num.toInt();
      } else if (inStart && num.length() > 0) {
        start_level = (uint8_t)num.toInt();
      }
      break;
    }

    // парсим координаты между p и s/e
    if (inCoords) {
      if (c == '-') {
        if (num.length() > 0) {
          coords[coords_length++] = (uint8_t)num.toInt();
          num = "";
        }
      } else if (isDigit(c)) {
        num += c;
      }
    }
    // парсим start_level после s
    else if (inStart) {
      if (isDigit(c)) {
        num += c;
      }
    }
  }
}



#endif
