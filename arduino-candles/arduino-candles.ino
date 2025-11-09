
#define RELAY_CANDLE_1 7
#define RELAY_CANDLE_2 2
#define RELAY_CANDLE_3 3
#define RELAY_FAIRYLIGHTS_4 4
#define RELAY_DIFFUSERS_5 5
#define RELAY_CRYSTALBALL_6 6
#define COMMS_PIN A2

void setup() {
  Serial.begin(9600);     
  delay(1000);           
  pinMode(RELAY_CANDLE_1, OUTPUT);
  pinMode(RELAY_CANDLE_2, OUTPUT);
  pinMode(RELAY_CANDLE_3, OUTPUT);
  pinMode(RELAY_FAIRYLIGHTS_4, OUTPUT);
  pinMode(RELAY_DIFFUSERS_5, OUTPUT);
  pinMode(RELAY_CRYSTALBALL_6, OUTPUT);
  pinMode(COMMS_PIN, INPUT_PULLUP);
}

void loop() {

  if(digitalRead(COMMS_PIN) == HIGH){
    runCandleSequence();
  }

  delay(1000); 

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

void runCandleSequence(){
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

  delay(3000);
  allOff();
}
