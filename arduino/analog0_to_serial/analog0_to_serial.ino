const int analogPin = A0; // Choose the analog pin you want to read

const int digitalPinRelayTV = 4;
const char ON_RELAY_TV_VALUE = '1';
const char OFF_RELAY_TV_VALUE = '0';
bool relayTVState = false;

const int digitalPinRelayLightRed = 2;
const int digitalPinRelayLightBlue = 3;

const char ON_RELAY_LIGHTS_VALUE = '3';
const char OFF_RELAY_LIGHTS_VALUE = '4';
const char BLINK_RELAY_LIGHTS_VALUE = '5';
bool relayLightsState = false;
bool blinkRelayLightsCounter = 2;
bool blinkingRelayLightsState = false;

void setup()
{

  Serial.begin(9600); // Set the baud rate for serial communication
  pinMode(digitalPinRelayTV, OUTPUT);
  pinMode(digitalPinRelayLightRed, OUTPUT);
  pinMode(digitalPinRelayLightBlue, OUTPUT);
}

void loop()
{
  int analogValue = analogRead(analogPin); // Read the value from the analog pin
  Serial.println(analogValue);             // Send the value through the serial port

  // Check if there is data available on the serial port
  while (Serial.available() > 0)
  {
    char command = Serial.read(); // Read the command sent by Python

    if (command == ON_RELAY_TV_VALUE)
    {
      relayTVState = true;
    }
    else if (command == OFF_RELAY_TV_VALUE)
    {
      relayTVState = false;
    }
    else if (command == ON_RELAY_LIGHTS_VALUE)
    {
      relayLightsState = true;
      blinkingRelayLightsState = false;
    }
    else if (command == OFF_RELAY_LIGHTS_VALUE)
    {
      relayLightsState = false;
      blinkingRelayLightsState = false;
    }
    else if (command == BLINK_RELAY_LIGHTS_VALUE)
    {
      relayLightsState != relayLightsState;
      blinkingRelayLightsState = true;
      blinkRelayLightsCounter = 2;
    }
  }

  if (blinkingRelayLightsState)
  {
    blinkRelayLightsCounter = blinkRelayLightsCounter - 1;
    if (blinkRelayLightsCounter <= 0)
    {
      relayLightsState = !relayLightsState;
      blinkRelayLightsCounter = 2;
    }
  }

  bool redState = relayLightsState;
  bool blueState = blinkingRelayLightsState ? !relayLightsState : relayLightsState;
  digitalWrite(digitalPinRelayLightRed, redState ? HIGH : LOW);
  digitalWrite(digitalPinRelayLightBlue, blueState ? HIGH : LOW);

  digitalWrite(digitalPinRelayTV, relayTVState ? HIGH : LOW);

  delay(100); // Wait 100 milliseconds before reading the value again
}