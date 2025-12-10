#include <Servo.h>

// Declare the Arduino pin where each servo is connected
#define SERVO_BASE_PIN 8
#define SERVO_SHOULDER_PIN 9
#define SERVO_ELBOW_PIN 10
#define SERVO_GRIPPER_PIN 11

// Define the start configuration of the joints
#define BASE_START 90
#define SHOULDER_START 90
#define ELBOW_START 90
#define GRIPPER_START 0

// LED pin
#define LED_PIN 13

// Register the servo motors of each joint
Servo base;  
Servo shoulder;  
Servo elbow;  
Servo gripper; 

uint8_t idx = 0;
uint8_t val_idx = 0;
char value[4] = "000";

// Blink timer variables
unsigned long lastBlink = 0;
bool ledState = false;

/*
 * Move a servo smoothly to the target angle.
 */
void reach_goal(Servo& motor, int goal){
  if(goal >= motor.read()){
    for (int pos = motor.read(); pos <= goal; pos++) { 
      motor.write(pos);     
      delay(15);                       
    }
  } else {
    for (int pos = motor.read(); pos >= goal; pos--) { 
      motor.write(pos);     
      delay(15);                       
    }
  }
}

void setup() {
  // Attach servos
  base.attach(SERVO_BASE_PIN);
  shoulder.attach(SERVO_SHOULDER_PIN);
  elbow.attach(SERVO_ELBOW_PIN);
  gripper.attach(SERVO_GRIPPER_PIN);

  // Initialize servo positions
  base.write(BASE_START);
  shoulder.write(SHOULDER_START);
  elbow.write(ELBOW_START);
  gripper.write(GRIPPER_START);

  // Start Serial
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Init LED pin
  pinMode(LED_PIN, OUTPUT);
}

void loop() {

  // -------------------------
  // 1-Second LED Blink
  // -------------------------
  unsigned long now = millis();
  if (now - lastBlink >= 1000) {   // One second passed
    ledState = !ledState;          // Toggle LED
    digitalWrite(LED_PIN, ledState);
    lastBlink = now;
  }

  // -------------------------
  // Serial Parsing for Servos
  // -------------------------
  if (Serial.available())
  {
    char chr = Serial.read();

    // base motor
    if(chr == 'b') { idx = 0; val_idx = 0; }

    // shoulder motor
    else if(chr == 's') { idx = 1; val_idx = 0; }

    // elbow motor
    else if(chr == 'e') { idx = 2; val_idx = 0; }

    // gripper motor
    else if(chr == 'g') { idx = 3; val_idx = 0; }

    // Separator between command and number
    else if(chr == ',')
    {
      int val = atoi(value);
      if(idx == 0) reach_goal(base, val);
      else if(idx == 1) reach_goal(shoulder, val);
      else if(idx == 2) reach_goal(elbow, val);
      else if(idx == 3) reach_goal(gripper, val);

      // Reset buffer
      value[0] = '0';
      value[1] = '0';
      value[2] = '0';
      value[3] = '\0';
    }

    // Numeric digits
    else
    {
      value[val_idx] = chr;
      val_idx++;
      if (val_idx > 2) val_idx = 2;  // prevent overflow
    }
  }
}
