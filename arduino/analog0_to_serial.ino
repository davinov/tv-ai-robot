const int analogPin = A0; // Choose the analog pin you want to read

void setup() {
  Serial.begin(9600); // Set the baud rate for serial communication
}

void loop() {
  int analogValue = analogRead(analogPin); // Read the value from the analog pin
  Serial.println(analogValue); // Send the value through the serial port
  delay(100); // Wait 100 milliseconds before reading the value again
}
