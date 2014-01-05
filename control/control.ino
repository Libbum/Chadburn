// Control code for the mechanical E.O.T.

// Currently just sends a random number between 1 and 11 
// through a serial connection every 10 seconds.

void setup() {
  Serial.begin(9600);
}

void loop() {
  int randNum = random(1, 11);
  Serial.println(randNum);

  delay(10000);
}
