#ifndef drivers
#define drivers


#include <ESP32Servo.h>

#define SERVO1_PIN 27 // up/down
#define SERVO2_PIN 26 // open/close

#define ENC_RIGHT_PIN 4
#define ENC_LEFT_PIN 5

#define MOTORL_PIN1 17
#define MOTORL_PIN2 16
#define MOTORR_PIN1 18
#define MOTORR_PIN2 19

#define SENSOR0_PIN 33
#define SENSOR1_PIN 32
#define SENSOR0_MIN 1500
#define SENSOR0_MAX 2920
#define SENSOR1_MIN 1666
#define SENSOR1_MAX 2940

#define SENSOR0_INVERT_MIN 2350
#define SENSOR0_INVERT_MAX 3950
#define SENSOR1_INVERT_MIN 2550
#define SENSOR1_INVERT_MAX 4050

Servo servo1, servo2;

volatile long encr = 0;
volatile long encl = 0;

int sensor_pins[] = { SENSOR0_PIN, SENSOR1_PIN };
int sensors_calib[] = { SENSOR0_MIN, SENSOR0_MAX, SENSOR1_MIN, SENSOR1_MAX };
int sensors_calib_invert[] = { SENSOR0_INVERT_MIN, SENSOR0_INVERT_MAX, SENSOR1_INVERT_MIN, SENSOR1_INVERT_MAX };


void callback_enc_right() {
  encr++;
}

void callback_enc_left() {
  encl++;
}

void drivers_init() {
  pinMode(SENSOR0_PIN, INPUT);
  pinMode(SENSOR1_PIN, INPUT);

  pinMode(MOTORL_PIN1, OUTPUT);
  pinMode(MOTORL_PIN2, OUTPUT);
  pinMode(MOTORR_PIN1, OUTPUT);
  pinMode(MOTORR_PIN2, OUTPUT);

  attachInterrupt(ENC_RIGHT_PIN, callback_enc_right, RISING);
  attachInterrupt(ENC_LEFT_PIN, callback_enc_left, RISING);

  servo2.attach(SERVO2_PIN);
  servo1.attach(SERVO1_PIN);
}


void print_default_sensors(uint8_t number) {
  int value = analogRead(sensor_pins[number]);
  Serial.println(value);
}

uint8_t sensors(uint8_t number) { // sensor number
  int value = analogRead(sensor_pins[number]);
  return constrain(map(value, sensors_calib[number * 2], sensors_calib[number * 2 + 1], 100, 0), 0, 100); // cast to range from 0 to 100
}

uint8_t sensors_invert(uint8_t number) { // sensor number
  int value = analogRead(sensor_pins[number]);
  return constrain(map(value, sensors_calib_invert[number * 2], sensors_calib_invert[number * 2 + 1], 100, 0), 0, 100); // cast to range from 0 to 100
}


void motors(int8_t power_l, int8_t power_r) {
  power_l = constrain(power_l, -100, 100);
  power_r = constrain (power_r, -100, 100);
  uint8_t left_pin1 = abs(power_l) * (power_l >= 0) * 2.55;
  uint8_t left_pin2 = abs(power_l) * (power_l < 0) * 2.55;
  analogWrite(MOTORL_PIN1, left_pin1);
  analogWrite(MOTORL_PIN2, left_pin2);
  uint8_t right_pin1 = abs(power_r) * (power_r >= 0) * 2.55;
  uint8_t right_pin2 = abs(power_r) * (power_r < 0) * 2.55;
  analogWrite(MOTORR_PIN1, right_pin1);
  analogWrite(MOTORR_PIN2, right_pin2);
}

void extra_stop() {
  delay(10);
  analogWrite(MOTORL_PIN1, 255);
  analogWrite(MOTORL_PIN2, 255);
  analogWrite(MOTORR_PIN1, 255);
  analogWrite(MOTORR_PIN2, 255);
  delay(300);
  motors(0, 0);
}

void stop_motors() {
  motors(-100, -100);
  delay(100);
  motors(0, 0);
}


void servo_down() {
  Serial.println("servo on - down");

//  servo1.attach(SERVO1_PIN);
//  delay(200);

  for (int i = 125; i > 60; i = i - 3) {
    servo1.write(i); // down
    delay(20);
  }
  delay(200);

//  delay(100);
//  servo1.detach();

  Serial.println("servo off - down");
}

void servo_up() {
  Serial.println("servo on - up");

//  servo1.attach(SERVO1_PIN);
//  delay(200);

  for (int i = 60; i < 125; i = i + 3) {
    servo1.write(i); // up
    delay(20);
  }
  delay(200);

//  delay(100);
//  servo1.detach();

  Serial.println("servo off - up");
}

void servo_open() {
  Serial.println("servo on - open");

//  servo2.attach(SERVO2_PIN);
//  delay(200);

  for (int i = 90; i > 50; i = i - 2) {
    servo2.write(i); // open
    delay(15);
  }

//  delay(100);
//  servo2.detach();

  Serial.println("servo off - open");
}

void servo_close() {
  Serial.println("servo on - close");

//  servo2.attach(SERVO2_PIN);
//  delay(200);

  for (int i = 50; i < 90; i = i + 2) {
    servo2.write(i); // close
    delay(15);
  }

//  delay(100);
//  servo2.detach();

  Serial.println("servo off - close");
}


#endif
