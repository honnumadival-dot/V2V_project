int buzzer = 5;

void setup() {
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    if (c == 'C') {
      digitalWrite(buzzer, HIGH); // danger
    } else {
      digitalWrite(buzzer, LOW);
    }
  }
}