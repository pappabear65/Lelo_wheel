import machine
import time
import micropython
import gc
import _thread
import secrets
### for connection to internet date & time and push to web page
import network
import builtins
import ntptime
import socket
import struct

# Nov 15
import uasyncio as asyncio
#

### for file size check
import os

### for ili9341 480x320 display

from ili934xnew import ILI9341, color565
import glcdfont
import tt14
import tt24
import tt32

# from math import isclose  #do not need right now

### might need to write data to sql server
# import urequests

sleeptime = 0.5

print("Objects loaded:")
time.sleep(sleeptime)

### set variables

fileSizeAtMax = 0
reed1TriggerTime = 0
reed1TriggerTimeLast = 0
reed1TriggerTimeDifference = 0
reed1TriggerTimeForDirection = 0
reed1triggerTimeEndOfSession = 0

reed2TriggerTime = 0
reed2TriggerTimeLast = 0
reed2TriggerTimeForDirection = 0

sessionRotationDirection = "tbd"
reedIdForFileWrite = "start up"
systemStatusForFileWrite = "pwr on"
sessionCounter = 0
sessionCounterFormatted = 0
reed1SessionRotationCounter = 0
reed2SessionRotationCounter = 0
distanceRunInSession = 0
distanceRunInSessionPrevious = 0
distanceRunInSessionFormatted = 0
distanceRunInDay = 0
distanceRunYesterdayLast = 0
distanceRunInDayFormatted = 0
distanceRunInDayDisplay = 0
distanceRunInDayDisplayFormatted = 0
distanceRunYesterday = 0
wheelCircumfrenceMeters = 0.86
secondsInAMilisecond = 0.001
digitRounding = 3
speedMetersPerSecond = 0
maxSpeedToday = 0
maxSpeedYesterday = 0
fileName = open("hamster_wheel_data.csv", "a")
inactivitySessionEndTime = 2000 #2500
sessionEndFlag = 1
timeSynchRefreshSeconds = 15 # ( 21600 = 6 hrs)

localDisplayTimeLast = 0
sessionCounterFormattedLast = 0
distanceRunInSessionFormattedLast = 0
sessionRotationDirectionLast = "tbd"
distanceRunInDayDisplayFormattedLast = 0
speedMetersPerSecondLast = 0
maxSpeedTodayLast = 0
maxSpeedYesterdayLast =0
firstRunEodFlag = 1
firstRunNtpFlag = 1
entryDateLast = "yyyy-mm-dd"
refreshNtpStartTime = 0

### set pins for reed switches and rotation indication LED
###  the LED goes on with reed 1 interupt and off with reed 2 interupt

activityLED = machine.Pin(15, machine.Pin.OUT)
activityLED.value(1)

reed1SpeedPin18 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
reed2DirectionPin21 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)
reed1Power = machine.Pin(19, machine.Pin.OUT)
reed1Power.value(1)
reed2Power = machine.Pin(20, machine.Pin.OUT)
reed2Power.value(1)

print("pins set:")
time.sleep(sleeptime)

### buffer for interupt handlers

micropython.alloc_emergency_exception_buf(100)

print("emergency ecception buffer set")
time.sleep(sleeptime)

### setting the display variables
### for some reason when put in a definition there are problems with sending data
### to the display.  Probably not passing variables to the rest of the system.
### doesn't hurt them to be here but after things are all working, it would not hurt to
### investigate further as more learning.

def setDisplayConfiguration():
    print("place holder, issues when used with display variables")

SCR_WIDTH = micropython.const(480)
SCR_HEIGHT = micropython.const(320)

# SCR_ROT:
# 0 = pico on top.
# 1 = horizontal, bb text up side right.
# 2 = pico on bottom.
# 3 = horizontal, bb text upside down

SCR_ROT = micropython.const(1)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

print(os.uname())
TFT_CLK_PIN = micropython.const(2)
TFT_MOSI_PIN = micropython.const(3)
TFT_MISO_PIN = micropython.const(4)
TFT_CS_PIN = micropython.const(5)
TFT_RST_PIN = micropython.const(7)
TFT_DC_PIN = micropython.const(6)

repeat_loop = 0
                
fonts = [glcdfont,tt14,tt24,tt32]

spi = machine.SPI(
    0,
    baudrate=40000000,
    miso=machine.Pin(TFT_MISO_PIN),
    mosi=machine.Pin(TFT_MOSI_PIN),
    sck=machine.Pin(TFT_CLK_PIN))

display = ILI9341(
    spi,
    cs=machine.Pin(TFT_CS_PIN),
    dc=machine.Pin(TFT_DC_PIN),
    rst=machine.Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.set_pos(0,0)
display.set_font(tt14)
# note: background colour initally set in ili934xnew.py
display.set_color(color565(0, 0, 0), color565(255, 255, 255))

print("display variables set")
time.sleep(sleeptime)

### set definitions:
###   set_position is in the format of horizontal, vertical for spacing.
###   each line is 25 pixels so increment vertical by 25 for each line.

def displayInitialization():

    ### Configure header
    display.set_pos(150,0)
    display.set_font(tt32)
    display.set_color(color565(255, 255, 0), color565(255, 255, 255))
    display.print("Lelo's exercise")

    ### Configure first line of data - date and time    
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,30)
    display.set_font(tt24)
    display.print("Date:")
    display.set_pos(240,30)
    display.print("Time:")
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,55)
    display.print(entryDate)
    display.set_pos(240,55)
    display.print(localDisplayTime)

    ### Configure second line of data - session number and rotation direction
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,80)
    display.print("Session number:")
    display.set_pos(240,80)
    display.print("Rotation direction:")    
    
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,105)
    display.print("0")    
    display.set_pos(240,105)
    display.print("tbd")

    ### Configure third line of data - current speed and distance in the session
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,130)
    display.print("Speed now m/s:")
    display.set_pos(240,130)
    display.print("Distance-session m:")

    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,155)
    display.print("0")
    display.set_pos(240,155)
    display.print("0")

    ### Configure fourth line of data - maximum speed today and distance run today
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,180)
    display.print("Max speed today m/s:")
    display.set_pos(240,180)
    display.print("Distance-today m:")    
    
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,205)
    display.print("0")    
    display.set_pos(240,205)
    display.print("0")

    ### Configure fifth line of data - maximum speed yesterday and distance yesterday.
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,230)
    display.print("max speed yesterday:")
    display.set_pos(240,230)
    display.print("distance yesterday:")
        
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,255)
    display.print("0")    
    display.set_pos(240,255)
    display.print("0")

def display_update():
    global entryDateLast
    global localDisplayTimeLast
    global sessionCounterFormattedLast
    global distanceRunInSessionFormattedLast
    global sessionRotationDirectionLast
    global distanceRunInDayDisplayFormattedLast
    global speedMetersPerSecondLast
    global maxSpeedTodayLast
    global maxSpeedYesterday
    global maxSpeedYesterdayLast
    global distanceRunYesterdayLast
    global distanceRunYesterday
    global wlan
    
    while True:
        
        gc.collect()
        setDateTime()
        
        ### blank out first line of data - date and time
        ### then rewrite it
        if entryDate != entryDateLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(0,55)
            display.print("..")
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))
            display.set_pos(0,55)
            display.print(entryDate)
            entryDateLast = entryDate
        if localDisplayTime != localDisplayTimeLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(240,55)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))            
            display.set_pos(240,55)
            display.print(str(localDisplayTime))
            localDisplayTimeLast = localDisplayTime        
        
        ### if changed, blank out second line of data - session number
        ### and rotation direction then rewrite it    
        if sessionCounterFormatted != sessionCounterFormattedLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(0,105)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))
            display.set_pos(0,105)
            display.print(str(sessionCounterFormatted))            
            sessionCounterFormattedLast = sessionCounterFormatted

        if sessionRotationDirection != sessionRotationDirectionLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(240,105)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))
            display.set_pos(240,105)
            display.print(str(sessionRotationDirection))
            sessionRotationDirectionLast = sessionRotationDirection

        ### blank out third line of data - current speed 
        ### and session distance then rewrite it          
        if speedMetersPerSecond != speedMetersPerSecondLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(0,155)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))            
            display.set_pos(0,155)
            display.print(str(speedMetersPerSecond))
            speedMetersPerSecondLast = speedMetersPerSecond

        if distanceRunInSessionFormatted != distanceRunInSessionFormattedLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(240,155)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))            
            display.set_pos(240,155)
            display.print(str(distanceRunInSessionFormatted))
            distanceRunInSessionFormattedLast = distanceRunInSessionFormatted

        ### blank out fourth line of data - maxium speed for day 
        ### and distance in day then rewrite it        
        if maxSpeedToday != maxSpeedTodayLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(0,205)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))
            display.set_pos(0,205)
            display.print(str(maxSpeedToday))
            maxSpeedTodayLast = maxSpeedToday

        if distanceRunInDayDisplayFormatted != distanceRunInDayDisplayFormattedLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(240,205)
            display.print("..")            
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))
            display.set_pos(240,205)
            display.print(str(distanceRunInDayDisplayFormatted))
            distanceRunInDayDisplayFormattedLast = distanceRunInDayDisplayFormatted
            
        ### blank out fifth line of data - maximum speed
        ### and total distance yesterday then rewrite it    
        if maxSpeedYesterday != maxSpeedYesterdayLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(0,255)
            display.print("..")
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))
            display.set_pos(0,255)
            display.print(str(maxSpeedYesterday))
            maxSpeedYesterdayLast = maxSpeedYesterday

        if distanceRunYesterday != distanceRunYesterdayLast:
            display.set_color(color565(255, 255, 255), color565(255, 255, 255))
            display.set_pos(240,255)
            display.print("..")  
            display.set_color(color565(255, 0, 255), color565(255, 255, 255))            
            display.set_pos(240,255)
            display.print(str(distanceRunYesterday))
            distanceRunYesterdayLast = distanceRunYesterday

        time.sleep(2)

### IP config on router assigns 192.168.0.118 to this pi-pico W.
def connect_wifi():
    global wlan
    
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

    entryTime = "hr:min:sec"
    localDisplayTime = "hr:min"
    entryDate = "yyyy-mm-dd"
    theDayOnly = "dd"
    theMonthOnly = "mm"
    theYearOnly = "yyyy"

def setDateTime():
    global entryTime
    global entryDate
    global localDisplayTime
    global theDayOnly 
    
    ### note: (hour + 2) is summer & (hour + 1) is winter in Sweden
 
    year, month, day, hour, minute, second, weekday, yearday = time.gmtime()
    entryDate = (f"{year:04}-{month:02}-{day:02}")
    entryTime = (f"{hour + 1}:{minute}:{second}")
    localDisplayTime = (f"{hour + 1:02}:{minute:02}")
    theDayOnly = (f"{day:02}")
    theMonthOnly = (f"{month:02}")
    theYearOnly = (f"{year:04}")

def file_size_check():
    
    gc.collect()
        
    global reedIdForFileWrite
    global systemStatusForFileWrite

    file_path = "/hamster_wheel_data.csv"

    try:
        file_size = os.stat(file_path)[6]
        gc.collect()
        max_memory = gc.mem_free() - 10000 #free_memory minus 10k to keep buffer available.
        if file_size < max_memory:
            setDateTime()
            log_reed_data()           
        else:
            fileSizeAtMax = 1
    except OSError:
        fileName = open("hamster_wheel_data.csv", "a")
        print("New data file created. ")

### Write data to the log file.

### This is where the data will sent to the SQL database.
### If database not available, can buffer some entries until it is.
### If file fills up, can let it stop logging as done in the file size
###  check routine now or wrap it around and put new data over old.
### Must look into this process, one piece at a time.

def log_reed_data():

    fileName.write("," + reedIdForFileWrite + "," +  str(entryDate) + "," + str(entryTime) + "," + systemStatusForFileWrite + "," + str(sessionCounter) + "," + str(reed1SessionRotationCounter) + "," + str(reed2SessionRotationCounter) + "," + str(sessionRotationDirection) + "," + str(reed1TriggerTime) + "," + str(reed1TriggerTimeLast) + "," + str(reed1TriggerTimeDifference) + "," + str(reed2TriggerTime) + "," + str(reed2TriggerTimeLast) + "," + str(speedMetersPerSecond) + "," + str(distanceRunInSession) + "\n")
            
    fileName.flush()
    
### IRQ callback function for reed_speed

def reed_speed_callback(pin):
   
    global reed1TriggerTime
    global reed1TriggerTimeLast
    global sessionCounter
    global sessionCounterFormatted
    global reed1SessionRotationCounter
    global sessionRotationDirection
    global reedIdForFileWrite
    global systemStatusForFileWrite
    global activityLED
    global sessionEndFlag
    global reed1TriggerTimeForDirection
    global reed2TriggerTimeForDirection

    activityLED.value(1)

    reed1TriggerTimeLast = reed1TriggerTime
    reed1TriggerTime = time.ticks_ms()

    
    if reed1SessionRotationCounter == 0:      

        sessionEndFlag = 0
        
        sessionCounter += 1
        sessionCounterFormatted = f"{sessionCounter:03}"
        
        reedIdForFileWrite = "reed 1"
        systemStatusForFileWrite = "start session"
              
        file_size_check()    

    if reed1TriggerTime != 0:

        ### reed 1 rotation count is used for calculating the distanced traveled in a
        ###  session which will help with speed calculations when used with trigger times
        ###  logged in data file. ideas, speed per revolution, average speed in session and possibly
        ###  acceleration / deceleration if ambitious.

        reed1SessionRotationCounter += 1

        reedIdForFileWrite = "reed 1"
        systemStatusForFileWrite = "in session"
        
        reed1TriggerTimeForDirection = reed1TriggerTime
        
        file_size_check()


### IRQ callback function for reed_direction

def reed_direction_callback(pin):    
    global reed2TriggerTime
    global reed2TriggerTimeLast
    global reed2SessionRotationCounter
    global sessionRotationDirection
    global reedIdForFileWrite
    global systemStatusForFileWrite
    global activityLED
    global reed1TriggerTimeForDirection
    global reed2TriggerTimeForDirection

    activityLED.value(0)

    reed2TriggerTimeLast = reed2TriggerTime
    reed2TriggerTime = time.ticks_ms()
   
    if reed2SessionRotationCounter == 0:      
                
        reedIdForFileWrite = "reed 2"
        systemStatusForFileWrite = "start session"
        
        file_size_check()
        
    if reed2TriggerTime != 0:
        
        reed2SessionRotationCounter += 1
        
        reedIdForFileWrite = "reed 2"
        systemStatusForFileWrite = "in session"
        
    if time.ticks_diff(reed2TriggerTime, reed1TriggerTime) > time.ticks_diff(reed1TriggerTime,reed2TriggerTimeLast):
        sessionRotationDirection = "cw"
    else:
        sessionRotationDirection ="cww"
        reed1TriggerTimeForDirection = 0
        reed2TriggerTimeForDirection = 0

    file_size_check()

def main():

    connect_wifi()
    print("WiFi connected")
    time.sleep(sleeptime)

    timeSynchronizationNTP()
    print("time set from NTP:")
    time.sleep(sleeptime)

    setDateTime()
    print("date and time set: ", entryDate, " ", entryTime, " ", time.gmtime())
    time.sleep(sleeptime)

    setDisplayConfiguration()
    print("Display Configured")
    time.sleep(sleeptime)
    
    displayInitialization()    
    print("display initialized")
    time.sleep(sleeptime) 

    ### Set IRQs for reed switch closing

    reed1SpeedPin18.irq(trigger=machine.Pin.IRQ_RISING, handler=reed_speed_callback)
    print("IRQ reed_speed set:")

    reed2DirectionPin21.irq(trigger=machine.Pin.IRQ_RISING, handler=reed_direction_callback)
    print("IRQ reed_direction set:")


    ### set initial trigger times

    reed1TriggerTime = time.ticks_ms()
    reed1TriggerTimeLast = reed1TriggerTime
    reed2TriggerTime = time.ticks_ms()
    reed2TriggerTimeLast = reed2TriggerTime

### if synchronizing the NTP time needs to be placed in
###  with the display update thread it needs to be incorporated with
###  a single definition for both the NTP and display. I think the definition
###  should be placed here.  also need to write it so it is looking for a flag
###  not based on time so it checks each time around compairing with
###  the time now and last time it was resynchronized.
###  Think we can set the flag for the first time synch up where the initial
###  NTP call is done as teh time sync is used regularly to make sure the correct
###  time stamp is in place.

### def core0_display_time_sync():
###     while True:
###         display_update()
###         timeSynchronizationNTP()

            ### refresh NTP every 6 hours
 
###         if firstRunNtpFlag == 1:
###             print("ignore me, first run")
###             refreshNtpStartTime = entryTime
###             firstRunNtpFlag = 0
###             time.sleep(2)
###         elif refreshNtpStartTime :
###             timeSynchronizationNTP()

    ### start new thread for the display hopefully to prevent issues with 
    ###  timing of the rest of the script.  Currently has a second delay between refreshes
    ###  also only updates parts where data has changed.
    ###  May also add the NTP time update to the thread.
    
    _thread.start_new_thread(display_update, ())

if __name__ == "__main__":
    main()

while True:

    ### calculations
    
    distanceRunInSession = builtins.round(wheelCircumfrenceMeters * reed1SessionRotationCounter,2)
    distanceRunInSessionFormatted = f"{distanceRunInSession:06}" 

    distanceRunInDayDisplay = builtins.round(distanceRunInDay + distanceRunInSession,2)
    distanceRunInDayDisplayFormatted =f"{distanceRunInDayDisplay:06}"

    reed1TriggerTimeDifference = abs(time.ticks_diff(reed1TriggerTime, reed1TriggerTimeLast))

    try:
        speedMetersPerSecond = builtins.round((wheelCircumfrenceMeters / (reed1TriggerTimeDifference * secondsInAMilisecond)),digitRounding)
    except:
        speedMetersPerSecond = 0
    else:
        # to ignore any glitches, 3 m/s is about 10 km/h, hamsters don't run that fast
        if speedMetersPerSecond >= 3:
            speedMetersPerSecond = 0
        elif speedMetersPerSecond > maxSpeedToday:
            maxSpeedToday = speedMetersPerSecond
    
    ### end of session check
    
    reed1triggerTimeEndOfSession = abs(time.ticks_diff(time.ticks_ms(), reed1TriggerTime))     

    if reed1triggerTimeEndOfSession > inactivitySessionEndTime and sessionEndFlag == 0:

        sessionEndFlag = 1
        
        distanceRunInDay = builtins.round(distanceRunInDay + distanceRunInSession,2)
        distanceRunInDayDisplay = distanceRunInDay
        distanceRunInDayDisplayFormatted =f"{distanceRunInDayDisplay:06}"

        reed1SessionRotationCounter = 0
        reed2SessionRotationCounter = 0
        speedMetersPerSecond = 0
        distanceRunInSession = 0
        
        reed1TriggerTimeForDirection = 0
        reed2TriggerTimeForDirection = 0
        
        sessionRotationDirection = "tbd"

        reedIdForFileWrite = "reed 1"
        systemStatusForFileWrite = "end session"
        reedIdForFileWrite = "reed 2"
        systemStatusForFileWrite = "end session"

        file_size_check()
  
    ### check for end of day
        
    if entryDate != entryDateLast and sessionEndFlag == 1:
        if firstRunEodFlag == 1:
            print("ignore me, first run")
            firstRunEodFlag = 0
            time.sleep(2)
        else:
            print("Test for date capture: ", str(entryDate), " ",str(entryDateLast), " ", str(sessionEndFlag))
            reed1SessionRotationCounter = 0
            reed2SessionRotationCounter = 0
            speedMetersPerSecond = 0
            maxSpeedYesterday = maxSpeedToday
            maxSpeedToday = 0
            distanceRunInSession = 0
            distanceRunYesterday = distanceRunInDayDisplayFormatted
            reed1TriggerTimeForDirection = 0
            reed2TriggerTimeForDirection = 0
            
            sessionRotationDirection = "tbd"

            reedIdForFileWrite = "reed 1"
            systemStatusForFileWrite = "end day"

            reedIdForFileWrite = "reed 2"
            systemStatusForFileWrite = "end day"
            
            file_size_check()
            
            ### pause to see if this will settle multiple hits when the dates don't match
            time.sleep(0.5)
            
            print("end of day detected")
            
        
###     machine.idle()  # can bed used to keep the program running 