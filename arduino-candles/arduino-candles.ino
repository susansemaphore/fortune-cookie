// === Relay Pin Definitions (verified against actual wiring) ===
#define RELAY_CANDLE_1     8    // Candles 1
#define RELAY_CANDLE_2     4    // Candles 2
#define RELAY_CANDLE_3     5    // Candles 3
#define RELAY_FAIRYLIGHTS_4 3   // Fairy lights
#define RELAY_DIFFUSERS_8  7    // Diffusers (confirmed!)
#define RELAY_CRYSTALBALL_7 11  // Crystal ball (confirmed)
#define COMMS_PIN A2            // Input from Uno

// === Setup ===
void setup() {
  Serial.begin(9600);
  delay(1000);

  pinMode(RELAY_CANDLE_1, OUTPUT);
  pinMode(RELAY_CANDLE_2, OUTPUT);
  pinMode(RELAY_CANDLE_3, OUTPUT);
  pinMode(RELAY_FAIRYLIGHTS_4, OUTPUT);
  pinMode(RELAY_DIFFUSERS_8, OUTPUT);
  pinMode(RELAY_CRYSTALBALL_7, OUTPUT);
  pinMode(COMMS_PIN, INPUT_PULLUP);

  allOff(); // ensure everything starts off

  // Serial.println("Running candle sequence once on startup:");
  // runCandleSequence();

  Serial.println("System ready.");
}


// === Main Loop ===
void loop() {

  // If Uno sends LOW, run the show
  if (digitalRead(COMMS_PIN) == LOW) {
    Serial.println("Trigger detected.");
    runCandleSequence();
  }

  delay(200); 
}


// === Helper Functions ===
void allOff() {
  switchRelay(RELAY_CANDLE_1, "off");
  switchRelay(RELAY_CANDLE_2, "off");
  switchRelay(RELAY_CANDLE_3, "off");
  switchRelay(RELAY_FAIRYLIGHTS_4, "on");
  switchRelay(RELAY_DIFFUSERS_8, "off");
  switchRelay(RELAY_CRYSTALBALL_7, "off");
}

void switchRelay(int relayPin, String state) {
  if (state == "on") {
    digitalWrite(relayPin, LOW);   // active LOW
  } else {
    digitalWrite(relayPin, HIGH);  // off
  }
}


// === Lighting & Effects Sequence ===
void runCandleSequence() {
  delay(3000);

  Serial.println("Candles 1 ON");
  switchRelay(RELAY_CANDLE_1, "on");
  delay(500);

  Serial.println("Candles 2 ON");
  switchRelay(RELAY_CANDLE_2, "on");
  delay(500);

  Serial.println("Candles 3 ON");
  switchRelay(RELAY_CANDLE_3, "on");
  delay(500);

  Serial.println("Fairy lights ON");
  switchRelay(RELAY_FAIRYLIGHTS_4, "on");

  Serial.println("Crystal ball ON");
  switchRelay(RELAY_CRYSTALBALL_7, "on");
  delay(500);

  Serial.println("Diffusers ON");
  switchRelay(RELAY_DIFFUSERS_8, "on");
  delay(3000);   // give them time to visibly start

  Serial.println("Diffusers OFF");
  switchRelay(RELAY_DIFFUSERS_8, "off");

  // Flicker fairy lights
  for (int i = 0; i < 12; i++) {
    switchRelay(RELAY_FAIRYLIGHTS_4, "on");
    delay(100);
    switchRelay(RELAY_FAIRYLIGHTS_4, "off");
    delay(100);
  }
  switchRelay(RELAY_FAIRYLIGHTS_4, "on");

  delay(3000);
  allOff();

  Serial.println("Sequence complete.");
}
