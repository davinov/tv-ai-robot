import serial
import time



THRESHOLD_VALUE = 1
GRACE_PERIOD_SECONDS = 1
SERIAL_RATE_MS = 100


current_state: bool = False
grace_period_counter: int = 0

def on_value_change(val: int):
    global grace_period_counter
    global current_state

    previous_state = current_state

    if val > THRESHOLD_VALUE:
        if not current_state:
            current_state = True
            grace_period_counter = int(GRACE_PERIOD_SECONDS * 1000 / SERIAL_RATE_MS)

    else:
        if grace_period_counter <= 0:
            current_state = False
        else:
            grace_period_counter = grace_period_counter - 1
    
    if previous_state != current_state:
        on_state_change(current_state)


def on_state_change(state: bool):
    if state:
        print('Start')
    else:
        print('Stop')


# Configure the serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace  with the appropriate port for your system
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
