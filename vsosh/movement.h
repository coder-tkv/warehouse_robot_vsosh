#ifndef movement
#define movement

#include "drivers.h"


#define GREY 40
uint8_t current_x = 0, current_y = 0, current_dir = 1, current_level = 0, ramps[10] = { 5, 11, 19, 20, 25, 29, 34, 46, 51, 54 }, numRamps_mv;


void if_cross(uint8_t power) {  //linefollow to cross
  float kp = 0.35, kd = 0.4, errold = 0;
  int power_l, power_r, s0, s1, err, u;
  bool exit = false;
  while (not exit) {
    s0 = sensors(0);
    s1 = sensors(1);
    err = s0 - s1;
    u = kp * err + kd * (err - errold);
    power_l = power + u;
    power_r = power - u;
    motors(power_l, power_r);
    errold = err;
    exit = (s0 < GREY) and (s1 < GREY);
    delay(1);
  }
}

void if_cross_invert(uint8_t power) {  //linefollow to cross
  float kp = 0.35, kd = 0.4, errold = 0;
  int power_l, power_r, s0, s1, err, u;
  bool exit = false;
  while (not exit) {
    s0 = sensors_invert(0);
    s1 = sensors_invert(1);
    err = s0 - s1;
    u = kp * err + kd * (err - errold);
    power_l = power - u;
    power_r = power + u;
    motors(power_l, power_r);
    errold = err;
    exit = (s0 > 100 - GREY) and (s1 > 100 - GREY);
    delay(1);
  }
}

void turn(int dir) {
  if (dir <= 1) {
    int encr_start = encr;
    int enc = 1000;
    while (encr < encr_start + enc) {
      motors(-22, 50);
    }
    extra_stop();
  } else if (dir == 3) {
    int encr_start = encr;
    int enc = 1170;
    while (encr < encr_start + enc) {
      motors(-50, 40);
    }
    extra_stop();
  } else {
    int encl_start = encl;
    int enc = 1100;
    while (encl < encl_start + enc) {
      motors(50, -22);
    }
    extra_stop();
  }
}

void if_encoder(uint8_t power, int enc) {  //linefollow to cross
  float kp = 0.3, kd = 0.4, errold = 0;
  int power_l, power_r, s0, s1, err, u;
  bool exit = false;
  int encr_start = encr;
  while (encr < encr_start + enc) {
    s0 = sensors(0);
    s1 = sensors(1);
    err = s0 - s1;
    u = kp * err + kd * (err - errold);
    power_l = power + u;
    power_r = power - u;
    motors(power_l, power_r);
    errold = err;
    delay(1);
  }
}

void if_encoder_invert(uint8_t power, int enc) {  //linefollow to cross
  float kp = 0.3, kd = 0.4, errold = 0;
  int power_l, power_r, s0, s1, err, u;
  bool exit = false;
  int encr_start = encr;
  while (encr < encr_start + enc) {
    s0 = sensors_invert(0);
    s1 = sensors_invert(1);
    err = s0 - s1;
    u = kp * err + kd * (err - errold);
    power_l = power - u;
    power_r = power + u;
    motors(power_l, power_r);
    errold = err;
    delay(1);
  }
}

int8_t sign(int8_t value) {
  return constrain(value, -1, 1);
}

void move(int coord1, int coord2, int axis_code) {

  if_encoder(40, 20);

  int destination_dir = 0;
  if (axis_code == 1 and coord2 - coord1 >= 0) {
    destination_dir = 3;
  } else if (axis_code == 1 and coord2 - coord1 < 0) {
    destination_dir = 1;
  } else if (axis_code == 0 and coord2 - coord1 >= 0) {
    destination_dir = 4;
  } else if (axis_code == 0 and coord2 - coord1 < 0) {
    destination_dir = 2;
  }

  int rotations = (5 + (current_dir - destination_dir)) % 4 - 1;
  if (rotations == 2) {
    turn(3);
  } else if (rotations == 0) {
    if_encoder(40, 400);
  } else {
    for (int i = 0; i < abs(rotations); i++) {
      int dir = (sign(rotations) + 3) / 2;
      turn(dir);
    }
  }

  current_dir = destination_dir;

  for (int i = 0; i < abs(coord2 - coord1); i++) {
    if (axis_code == 0 and coord2 > coord1) {
      current_x++;
    } else if (axis_code == 0 and coord2 < coord1) {
      current_x--;
    } else if (axis_code == 1 and coord2 > coord1) {
      current_y++;
    } else if (axis_code == 1 and coord2 < coord1) {
      current_y--;
    }

    if_cross(40);
    if (i != abs(coord2 - coord1) - 1) {
      if_encoder(40, 400);
    }
    extra_stop();
  }
}

void navigation(uint8_t destination_x, uint8_t destination_y) {
  if (current_y != destination_y) {
    move(current_y, destination_y, 1);
    extra_stop();
  }
  if (current_x != destination_x) {
    move(current_x, destination_x, 0);
    extra_stop();
  }
}



#endif
