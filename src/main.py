from typing import Literal
import serial
import time

ARDUINO_SERIAl_PORT = '/dev/ttyACM0'

ON_RELAY_TV_VALUE = b'1'
OFF_RELAY_TV_VALUE = b'0'

ON_RELAY_LIGHTS_VALUE = b'3'
OFF_RELAY_LIGHTS_VALUE = b'4'
BLINK_RELAY_LIGHTS_VALUE = b'5'


THRESHOLD_VALUE = 10
GRACE_PERIOD_SECONDS = 2
SERIAL_RATE_MS = 100


current_tv_state: bool = False
grace_period_counter: int = 0
current_lights_state: bool | Literal['blink'] = False

def on_value_change(val: int):
    global grace_period_counter
    global current_tv_state
    global current_lights_state

    previous_tv_state = current_tv_state
    previous_lights_state = current_lights_state

    if val > THRESHOLD_VALUE:
        if not current_tv_state:
            current_tv_state = True
            
        if current_lights_state != True:
            current_lights_state = True
            grace_period_counter = int(GRACE_PERIOD_SECONDS * 1000 / SERIAL_RATE_MS)

    else:
        if grace_period_counter <= 0:
            current_tv_state = False
            current_lights_state = False
        else:
            grace_period_counter = grace_period_counter - 1
            current_lights_state = 'blink'
    
    if previous_tv_state != current_tv_state:
        on_state_tv_change(current_tv_state)
    
    if previous_lights_state != current_lights_state:
        on_state_lights_change(current_lights_state)


def on_state_tv_change(tv_state: bool):
    if tv_state:
        print('Start TV')
        ser.write(ON_RELAY_TV_VALUE)
    else:
        print('Stop TV')
        ser.write(OFF_RELAY_TV_VALUE)


def on_state_lights_change(lights_state: bool | Literal['blink']):
    match lights_state:
        case True:
            print('Start lights')
            ser.write(ON_RELAY_LIGHTS_VALUE)
        case 'blink':
            print('Blink lights')
            ser.write(BLINK_RELAY_LIGHTS_VALUE)
        case False:
            print('Stop lights')
            ser.write(OFF_RELAY_LIGHTS_VALUE)


# Configure the serial port and baud rate
ser = serial.Serial(ARDUINO_SERIAl_PORT, 9600)  # Replace  with the appropriate port for your system
time.sleep(2)  # Wait for the serial connection to initialize

while True:
    try:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        
        # Convert the received data to an integer
        analog_value = int(line or 0)
        
        # Do something with the analog value
        # print(f"Analog value: {analog_value}")
        on_value_change(analog_value)
    
    except Exception as e:
        print(f"Error: {e}")
        break

# Close the serial connection
ser.close()
