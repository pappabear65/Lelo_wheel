# When planning a MicroPython project for the Raspberry Pi Pico W, especially one with multiple modules
# and functionalities, it's important to follow a structured methodology to ensure the project is
# organized, maintainable, and scalable. Here is a suggested approach, breaking down the project into
# modules and providing guidelines for each.
# 
# Project Structure
# 
#     Project Directory Layout:
# 
#     Organize your project into directories to separate different functionalities.
#     Use a main.py or boot.py file for the entry point of your project.

# my_project/
# ├── main.py
# ├── boot.py (this is an alternate to main.py.  Use one or the other)
# ├── lib/
# │   ├── __init__.py  (sets initial working state?  set up pins, variables??)
# │   ├── data_collection.py
# │   ├── data_validation.py
# │   ├── calculations.py
# │   ├── data_storage.py
# │   ├── web_server.py
# │   └── utils.py
# ├── config/
# │   ├── config.py
# └── data/
#     ├── logs/
#     ├── daily/
#     ├── weekly/
#     ├── monthly/
#     └── yearly/
    

# Modules and Their Responsibilities
# 
# 1) Data Collection (data_collection.py):
# 
#     Responsible for collecting data from sensors or other input sources.
#     Use functions or classes to abstract the data collection logic.

# data_collection.py
import machine

def read_temperature():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature

# 2) Data Validation (data_validation.py):
# 
#     Ensures the collected data is within expected ranges and formats.
#     Implements validation functions.

# data_validation.py
def validate_temperature(temp):
    if -40 <= temp <= 125:
        return True
    return False

# 3) Calculations (calculations.py):
# 
#     Performs necessary calculations on the collected data.
#     Can include averaging, statistical analysis, etc.

# calculations.py
def average(values):
    return sum(values) / len(values)

# 4) Data Storage (data_storage.py):
# 
#     Handles storing data locally or remotely.
#     Organizes data into daily, weekly, monthly, and yearly directories.

# data_storage.py
import uos

def store_data(data, path):
    with open(path, 'a') as f:
        f.write(data + '\n')
        
# 5) Web Server (web_server.py):
# 
#     Serves the collected and processed data to a webpage.
#     Manages WebSocket or HTTP communication.

# web_server.py
import socket

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = html_page()
        cl.send(response)
        cl.close()

def html_page():
    return b"""HTTP/1.1 200 OK
    Content-Type: text/html

    <!DOCTYPE html>
    <html>
    <head><title>Pico W</title></head>
    <body>
    <h1>Data from Pico W</h1>
    <p>Temperature: -- °C</p>
    </body>
    </html>
    """

# 6) Utility Functions (utils.py):
# 
#     Contains helper functions that are used across multiple modules.
#     Examples: logging, time formatting, configuration loading.

# utils.py
import time

def log(message):
    with open('data/logs/log.txt', 'a') as f:
        f.write(f"{time.localtime()}: {message}\n")

# 7) Configuration (config.py):
# 
#     Centralized configuration settings for the project.
#     Includes Wi-Fi credentials, file paths, thresholds, etc.

# config.py
WIFI_SSID = 'your_ssid'
WIFI_PASSWORD = 'your_password'
DATA_PATH = 'data/'

# 8) Entry Point (main.py)
#
#     Coordinates the execution of different modules.
#     Initializes the system, sets up connections, and starts the main loop.

# main.py
import time
import network
from lib.data_collection import read_temperature
from lib.data_validation import validate_temperature
from lib.data_storage import store_data
from lib.web_server import start_server
from lib.utils import log
from config.config import WIFI_SSID, WIFI_PASSWORD, DATA_PATH

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    print('Connected:', wlan.ifconfig())

def main():
    connect_wifi()
    log("System initialized")
    start_server()
    
    while True:
        temp = read_temperature()
        if validate_temperature(temp):
            data_path = DATA_PATH + 'daily/data.txt'
            store_data(f"{time.localtime()}: {temp}", data_path)
            log(f"Data stored: {temp} °C")
        else:
            log("Invalid temperature data")
        time.sleep(5)  # Collect data every 5 seconds

if __name__ == "__main__":
    main()

# 9) Additional Considerations:
#     
#     Concurrency: Since the Pico W has two cores, you can use MicroPython's _thread module to handle
#     concurrent tasks. For example, one core can handle data collection and processing,
#     while the other handles the web server.

import _thread

def data_task():
    while True:
        temp = read_temperature()
        if validate_temperature(temp):
            data_path = DATA_PATH + 'daily/data.txt'
            store_data(f"{time.localtime()}: {temp}", data_path)
            log(f"Data stored: {temp} °C")
        else:
            log("Invalid temperature data")
        time.sleep(5)

def web_task():
    start_server()

_thread.start_new_thread(data_task, ())
_thread.start_new_thread(web_task, ())


# 10) Error Handling:
#     
#     Implement robust error handling in all modules to ensure the system is resilient and can recover from unexpected issues.
# 
# 11) Testing:
#     
#     Thoroughly test each module independently before integrating them into the main project.
