const int analogPin = A0; // Choose the analog pin you want to read

const int digitalPinRelayTV = 4;

bool relayTVState = false;

const int digitalPinRelayLightRed = 2;
const int digitalPinRelayLightBlue = 3;

const char ON_RELAY_TV_CMD[] = "tv:on";
const char OFF_RELAY_TV_CMD[] = "tv:off";
const char ON_RELAY_LIGHTS_CMD[] = "lights:on";
const char OFF_RELAY_LIGHTS_CMD[] = "lights:off";
const char BLINK_RELAY_LIGHTS_CMD[] = "lights:blink";

String SETUP_BLINK_RELAY_COUNTER_CMD = "set:blink_relay_counter:";
int BLINK_RELAY_COUNTER_VALUE = 5;

bool relayLightsState = false;
int blinkRelayLightsCounter = BLINK_RELAY_COUNTER_VALUE;
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
  Serial.println("A0:" + String(analogValue));             // Send the value through the serial port

  // Check if there is data available on the serial port
  while (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n'); // Read the command sent by Python
    Serial.println("Command:");
    Serial.println(command);

    if (command.startsWith(SETUP_BLINK_RELAY_COUNTER_CMD)) {
      BLINK_RELAY_COUNTER_VALUE = command.substring(SETUP_BLINK_RELAY_COUNTER_CMD.length()).toInt();
      Serial.println("Debug: set val to:" + String(BLINK_RELAY_COUNTER_VALUE));
    }
    else if (command == ON_RELAY_TV_CMD)
    {
      relayTVState = true;
    }
    else if (command == OFF_RELAY_TV_CMD)
    {
      relayTVState = false;
    }
    else if (command == ON_RELAY_LIGHTS_CMD)
    {
      relayLightsState = true;
      blinkingRelayLightsState = false;
    }
    else if (command == OFF_RELAY_LIGHTS_CMD)
    {
      relayLightsState = false;
      blinkingRelayLightsState = false;
    }
    else if (command == BLINK_RELAY_LIGHTS_CMD)
    {
      relayLightsState != relayLightsState;
      blinkingRelayLightsState = true;
      blinkRelayLightsCounter = BLINK_RELAY_COUNTER_VALUE;
    }
    else {
      // Setup
      // if (command == SETUP_CMD){
      //   if (Serial.available() >= 2) {
      //     char cmd = Serial.read();
      //     if (cmd == SETUP_BLINK_RELAY_COUNTER_CMD) {
      //       BLINK_RELAY_COUNTER_VALUE = (int) Serial.read();
      //     }
      //   }
      // }
    }
  }

  if (blinkingRelayLightsState)
  {
    blinkRelayLightsCounter = blinkRelayLightsCounter - 1;
    if (blinkRelayLightsCounter <= 0)
    {
      relayLightsState = !relayLightsState;
      blinkRelayLightsCounter = BLINK_RELAY_COUNTER_VALUE;
    }
  }

  bool redState = relayLightsState;
  bool blueState = blinkingRelayLightsState ? !relayLightsState : relayLightsState;
  digitalWrite(digitalPinRelayLightRed, redState ? HIGH : LOW);
  digitalWrite(digitalPinRelayLightBlue, blueState ? HIGH : LOW);

  digitalWrite(digitalPinRelayTV, relayTVState ? HIGH : LOW);

  delay(100); // Wait 100 milliseconds before reading the value again
}