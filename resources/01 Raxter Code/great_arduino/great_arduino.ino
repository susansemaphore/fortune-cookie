#include <Servo.h>

#define RELAY_CANDLE_1 7
#define RELAY_CANDLE_2 2
#define RELAY_CANDLE_3 3
#define RELAY_FAIRYLIGHTS_4 4
#define RELAY_DIFFUSERS_5 5
#define RELAY_CRYSTALBALL_6 6
#define SERVO_PIN 9

#define OPEN_ANGLE 90
#define CLOSE_ANGLE 180
Servo myservo;

void setup() {
  Serial.begin(9600);     
  delay(1000);           
  
  pinMode(RELAY_CANDLE_1, OUTPUT);
  pinMode(RELAY_CANDLE_2, OUTPUT);
  pinMode(RELAY_CANDLE_3, OUTPUT);
  pinMode(RELAY_FAIRYLIGHTS_4, OUTPUT);
  pinMode(RELAY_DIFFUSERS_5, OUTPUT);
  pinMode(RELAY_CRYSTALBALL_6, OUTPUT);
  myservo.attach(SERVO_PIN);
}

void loop() {
   if (Serial.available() > 0) { // Check if data is available
    char command = Serial.read(); // Read the incoming byte
    if (command == '1') {
      
      moveServo(OPEN_ANGLE);      // Move to 0 degrees
      delay(3000);
      switchRelay(RELAY_FAIRYLIGHTS_4, "on");
      delay(500);
    }
    if (command == '2') {
      
      moveServo(OPEN_ANGLE);      // Move to 0 degrees
      delay(3000);
      switchRelay(RELAY_CANDLE_1, "on");
      delay(500);  
      switchRelay(RELAY_CANDLE_2, "on");
      delay(500);  
      switchRelay(RELAY_CANDLE_3, "on");
      delay(500);  
      switchRelay(RELAY_FAIRYLIGHTS_4, "on");
      switchRelay(RELAY_CRYSTALBALL_6, "on");
      delay(500);  
      switchRelay(RELAY_DIFFUSERS_5, "on");
      delay(500);  
      switchRelay(RELAY_DIFFUSERS_5, "off");
      for (int i = 0 ; i < 10 ; i++)
      {
        switchRelay(RELAY_FAIRYLIGHTS_4, "on");
        delay(100);
        switchRelay(RELAY_FAIRYLIGHTS_4, "off");
        delay(100);
      }
      switchRelay(RELAY_FAIRYLIGHTS_4, "on");
    }
    if (command == '3') {
      
      delay(1000);
      allOff();
    //if (command == '1') {
      delay(1000); 
      moveServo(CLOSE_ANGLE);    // Move to 180 degrees
      delay(3000); 
    }
  }
    //}
  delay(200);
}

void allOff()
{
  switchRelay(RELAY_CANDLE_1, "off");
  switchRelay(RELAY_CANDLE_2, "off");
  switchRelay(RELAY_CANDLE_3, "off");
  switchRelay(RELAY_FAIRYLIGHTS_4, "off");
  switchRelay(RELAY_DIFFUSERS_5, "off");
  switchRelay(RELAY_CRYSTALBALL_6, "off");
  switchRelay(RELAY_CANDLE_3, "off");   // Relay OFF
}

void switchRelay(int relayPin, String state) {
  if (state == "on" || state == "ON") {
    digitalWrite(relayPin, LOW);
  }
  if (state == "off" || state == "OFF") {
    digitalWrite(relayPin, HIGH);
  }
}

void moveServo(int angle) {
  // Ensure angle is between 0 and 180
  angle = constrain(angle, 0, 180);
  myservo.write(angle);
}
//Servo wires:
//  Brown/Black → GND (on power supply)
//  Red → 5V (on power supply)
//  Orange/Yellow → Signal (to SERVO_PIN on Arduino)
//Connect Arduino GND to power supply GND