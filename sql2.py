import urequests
import json
import time
import network
import socket
import struct
import builtins
import ure as re
import ustruct
import ubinascii
import hashlib
from machine import ADC

# Initialize temperature sensor
sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)

timestamp = "A"
loc_date = 0
loc_time = 0

#############################
##### set time from NTP #####
#############################


NTP_DELTA = 2208988800
host = "pool.ntp.org"

led = machine.Pin("LED", machine.Pin.OUT)

ssid = 'ekdahl_2.4'
password = '60493999100324656048737966'

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    print(wlan.ifconfig())


led.on()
set_time()
print("NTP time set ",time.gmtime())
led.off()


print("time set from NTP:")
time.sleep(2)

###############################
##### end of setting time #####
###############################

def date_time():
    global loc_time
    global loc_date

####
#note: hour + 2 is summer time in Sweden gmt+2
#find solution to change with dst in spring and fall
####

    year, month, day, hour, minute, second, weekday, yearday = time.gmtime()
    loc_date = (f"{day}/{month}/{year}")
    loc_time = (f"{hour + 2}:{minute}:{second}")

date_time()
# print("date and time set: ", loc_date, " ", loc_time, " ", time.gmtime())
time.sleep(2)

########
url = 192.168.0.111
urequests.get(192.168.0.111,**kw)
#########

def read_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = (27 - (reading - 0.706) / 0.001721)

    print("temp ",temperature)
    return temperature

# def send_data_to_server(temperature, loc_date, loc_time):
#     url = "http://192.168.0.111:3306/mysql/my_temp/pi_temp/"
#     data = {
#         "temperature": temperature,
#         "loc_date": loc_date,
#         "loc_time": loc_time
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = urequests.post(url, data=json.dumps(data), headers=headers)
#     print(response.text)
#     response.close()

def send_data_to_server(temperature, loc_date, loc_time):
    url = "http://192.168.0.111:3306/my_temp/"
    data = {
        
        "loc_time": loc_time,
        "loc_date": loc_date,
        "temperature": int(temperature)
        
    }
    headers = {
        "Content-Type": "application/json"
    }
    print("headers ", headers)
    print("data ", data, json.dumps(data))
    
    response = urequests.post(url, data=json.dumps(data), headers=headers)
    print("data 2 ", data)
    print(response.text)
    response.close()

# Main loop
while True:
    temperature = read_temperature()
#    temperature = int(temp)
    date_time()  # Get current time

    print(temperature)
    print(loc_date, loc_time)

    send_data_to_server(temperature, loc_date, loc_time)
    time.sleep(10)  # Send data every 10 seconds

##########
    
# def read_temperature():
#     reading = sensor_temp.read_u16() * conversion_factor
#     temperature = int(27 - (reading - 0.706) / 0.001721)
#     return temperature
# 
# def send_data_to_server(temperature, loc_date, loc_time):
#     url = "http://192.168.0.111:3306/mysql/my_temp/pi_temp/"
#     data = {
#         "temperature": temperature,
#         "loc_date": loc_date,
#         "loc_time": loc_time
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = urequests.post(url, data=json.dumps(data), headers=headers)
#     print(response.text)
#     response.close()
# 
# # Main loop
# while True:
#     temperature = read_temperature()
# #    temperature = int(temp)
#     date_time()  # Get current time
# 
#     print(temperature)
#     print(loc_date, loc_time)
# 
#     send_data_to_server(temperature, loc_date, loc_time)
#     time.sleep(10)  # Send data every 10 seconds




####and another####

# import urequests
# import json
# 
# def send_data_to_server(temperature, timestamp):
#     url = "http://<server-ip>:5000/log"
#     data = {
#         "temperature": temperature,
#         "timestamp": timestamp
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = urequests.post(url, data=json.dumps(data), headers=headers)
#     print(response.text)
#     response.close()

