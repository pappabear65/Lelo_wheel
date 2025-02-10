import machine
import time
import json
import builtins
import network
import ntptime
import secrets

sleeptime = 1

# General settings
prog_name = "pilogger2.py"

# Settings for database connection
hostname = secrets.sql_secrets["hostname"]
username = secrets.sql_secrets["username"]
password = secrets.sql_secrets["password"]
database = secrets.sql_secrets["database"]


def connect_wifi():
    global wlan
    # IP config on router assigns 192.168.0.118 to this pi-pico W.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.network_secrets["ssid"],secrets.network_secrets["password"])
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi")
    print("IP Address:", wlan.ifconfig()[0])

def timeSynchronizationNTP():
    try:
        ntptime.settime()
        print("Time synchronized with NTP server")
    except Exception as e:
        print("Failed to sync time: ", e)

    localTime = "hr:min:sec"
    localDisplayTime = "hr:min"
    localDate = "yyyy-mm-dd"
    todayDayOnly = "dd"

def setDateTime():
    global localTime
    global localDate
    global localDisplayTime
    global todayDayOnly
    
####
#note: (hour + 2) is summer & (hour + 1) is winter in Sweden
####
 
    year, month, day, hour, minute, second, weekday, yearday = time.gmtime()
    localDate = (f"{year:04}/{month:02}/{day:02}")
    localTime = (f"{hour + 1}:{minute}:{second}")
    localDisplayTime = (f"{hour + 1:02}:{minute:02}")
    todayDayOnly = (f"{day:02}")
#    print(str(localDate))

connect_wifi()
print("WiFi connected")
time.sleep(sleeptime)

timeSynchronizationNTP()
print("time set from NTP:")
time.sleep(sleeptime)

setDateTime()
print("date and time set: ", localDate, " ", localTime, " ", time.gmtime())
time.sleep(sleeptime)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
 
while True:
    setDateTime()
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = builtins.round(27 - (reading - 0.706)/0.001721,2)
    print("Temperature: {}".format(temperature), " date: ", str(localDate), " time: ", str(localTime))
    time.sleep(2)

# 
# 
# dht_sensor_port = 4                     # Connect the DHT sensor to port D
# dht_sensor_type = Adafruit_DHT.DHT11    # Sensor type
# 
# device = 'pi-003'                        # Host name of the Pi
# 
# GPIO.setmode(GPIO.BCM)                  # Use the Broadcom pin numbering
# GPIO.setup(led, GPIO.OUT)               # LED pin set as output
# GPIO.setup(dht_sensor_port, GPIO.IN)    # DHT sensor port as input
# 
# # Routine to insert temperature records into the pidata.temps table:
# def insert_record( device, datetime, temp, hum ):
#     query = "INSERT INTO temps3 (device,datetime,temp,hum) " \
#                 "VALUES (%s,%s,%s,%s)"
#         args = (device,datetime,temp,hum)
# 
#         try:
#             conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
#         cursor = conn.cursor()
#             cursor.execute(query, args)
#         conn.commit()
# 
#         except Exception as error:
#             print(error)
# 
#         finally:
#             cursor.close()
#             conn.close()
# 
# # Print welcome 
# print('[{0:s}] starting on {1:s}...'.format(prog_name, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
# 
# # Main loop
# try:
#     while True:
#         hum, temp = Adafruit_DHT.read_retry(dht_sensor_type, dht_sensor_port)
#         temp = temp * 9/5.0 + 32
#         now = datetime.datetime.now()
#         date = now.strftime('%Y-%m-%d %H:%M:%S')
#         insert_record(device,str(date),format(temp,'.2f'),format(hum,'.2f'))
#         time.sleep(180)
# 
# except (IOError,TypeError) as e:
#     print("Exiting...")
# 
# except KeyboardInterrupt:  
#         # here you put any code you want to run before the program   
#         # exits when you press CTRL+C  
#     print("Stopping...")
# 
# finally:
#     print("Cleaning up...")  
#     GPIO.cleanup() # this ensures a clean exit