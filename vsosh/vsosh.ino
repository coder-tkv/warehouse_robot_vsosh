#include "drivers.h"
#include "movement.h"
#include "bluetooth.h"

uint8_t routeCoords[64];
uint8_t routeLen = 0;
uint8_t start_level = 0;

void setup() {
  drivers_init();
  Serial.begin(115200);
}

void loop() {

  String route = receiveRoute();
  Serial.println(route);
  parseRouteString(route, routeCoords, routeLen, start_level);


  Serial.println("=== Parsed Route ===");

  current_x = routeCoords[0] % 4;
  current_y = routeCoords[0] / 4;

  Serial.print("Path: ");
  for (int j = 0; j < routeLen; j++) {
    uint8_t local_x = routeCoords[j] % 4;
    uint8_t local_y = routeCoords[j] / 4;

    Serial.print("(");
    Serial.print(local_x);
    Serial.print(",");
    Serial.print(local_y);
    Serial.print(")");
    navigation(local_x, local_y);
  }
  Serial.println();

  Serial.println("====================");

}
