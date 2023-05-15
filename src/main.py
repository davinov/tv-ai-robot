from typing import Literal
import serial
import time
from singletonprocess import SingletonProcess
#from pyhacktv import HackTV

run = True
PLAYLIST_VIDEOS = '/usr/share/robot-playlist'
ARDUINO_SERIAl_PORT = '/dev/arduino'

SET_BLINK_TIME = 'set:blink_relay_counter:'

ON_RELAY_TV_VALUE = 'tv:on'
OFF_RELAY_TV_VALUE = 'tv:off'

ON_RELAY_LIGHTS_VALUE = 'lights:on'
OFF_RELAY_LIGHTS_VALUE = 'lights:off'
BLINK_RELAY_LIGHTS_VALUE = 'lights:blink'


THRESHOLD_VALUE = 20
GRACE_PERIOD_SECONDS = 3
BLINK_RELAY_COUNTER_VALUE = 600 # in ms
SERIAL_RATE_MS = 100

#h: HackTV = HackTV()
h: SingletonProcess = SingletonProcess()
current_tv_state: bool = False
grace_period_counter: int = 0
current_lights_state: bool | Literal['blink'] = False


def send_to_arduino(command: str):
    ser.write((command + '\n').encode(encoding = 'ascii', errors = 'strict'))

def setup():
    print('Sending command')
    send_to_arduino(f'{SET_BLINK_TIME}{int(BLINK_RELAY_COUNTER_VALUE / SERIAL_RATE_MS)}')


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

import os
import random

def select_random_file(directory):
    # Obtient une liste de tous les fichiers dans le répertoire
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Sélectionne un fichier au hasard
    selected_file = random.choice(files)
    
    # Retourne le chemin complet du fichier sélectionné
    return os.path.join(directory, selected_file)



def on_state_tv_change(tv_state: bool):
    if tv_state:
        print('Start TV')
        send_to_arduino(ON_RELAY_TV_VALUE)
        #h.start("/home/david/Documents/Robot/10s.mp4")
        random_file = select_random_file(PLAYLIST_VIDEOS)
        print("start %s" % random_file)
        #h.start("/usr/local/bin/hacktv","-m", "l", "-f", "471250000", "-s", "16000000", "-g", "30", "-v", "--nonicam", "--nocolour", random_file)
        ff = 'ffmpeg:%s' % random_file
        h.start("/usr/local/bin/hacktv","-m", "l", "-f", "471250000", "-s", "16000000", "-g", "30", "-v", "--nonicam", "--nocolour", ff)
    else:
        print('Stop TV')
        send_to_arduino(OFF_RELAY_TV_VALUE)
        h.stop()
        # h.start("/usr/local/bin/hacktv","-m", "l", "-f", "471250000", "-s", "16000000", "-g", "30", "-v", "--nonicam", "--nocolour", "test:colourbars")



def on_state_lights_change(lights_state: bool | Literal['blink']):
    match lights_state:
        case True:
            print('Start lights')
            send_to_arduino(ON_RELAY_LIGHTS_VALUE)
        case 'blink':
            print('Blink lights')
            send_to_arduino(BLINK_RELAY_LIGHTS_VALUE)
        case False:
            print('Stop lights')
            send_to_arduino(OFF_RELAY_LIGHTS_VALUE)

#h.start("hackrf_info")
h.start("/usr/local/bin/hacktv","-m", "l", "-f", "471250000", "-s", "16000000", "-g", "30", "-v", "--nonicam", "--nocolour", "test:colourbars")

# Configure the serial port and baud rate
ser = serial.Serial(ARDUINO_SERIAl_PORT, 9600)  # Replace  with the appropriate port for your system
time.sleep(2)  # Wait for the serial connection to initialize

print("Setup start")
setup()
print("Setup done")

count: int = 0

while run:
    try:
        count += 1

        # Read a line from the serial port
        line = ser.readline().decode(encoding='ascii', errors='strict').strip()
                
        # Convert the received data to an integer
        if line.startswith('A0:'):
            analog_value = int(line[3:] or 0)
            # Do something with the analog value
            #print(f"Analog value: {analog_value}")
            on_value_change(analog_value)
        else:
            print('Debug: ', line)

        #if count % 10 == 0:
        #    count = 0
        #    print(analog_value)
        
    
    except Exception as e:
        print(f"Error: {e}")
        run = False
        h.stop()
        break
# Close the serial connection
ser.close()
