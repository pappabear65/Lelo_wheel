from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time
from random import randint 

SCR_WIDTH = const(480)
SCR_HEIGHT = const(320)

# SCR_ROT:
# 0 = pico on top.
# 1 = horizontal, bb text up side right.
# 2 = pico on bottom.
# 3 = horizontal, bb text upside down

SCR_ROT = const(1)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

print(os.uname())
TFT_CLK_PIN = const(2)
TFT_MOSI_PIN = const(3)
TFT_MISO_PIN = const(4)
TFT_CS_PIN = const(5)
TFT_RST_PIN = const(7)
TFT_DC_PIN = const(6)

repeat_loop = 0

# The origional software example had assigned incorrect pins for the display
# on the pico breadboard kit. Proper values in use.
# Here are the TFT controller values from the breadboard:
#
# sclk gp2
# mosi gp3
# miso gp4
# cs gp5
# dc gp6
# rst gp7
# tprst gp10
# tpint gp11
# i2c gp8 gp9

# load fonts
                
fonts = [glcdfont,tt14,tt24,tt32]
text = 'No! not you again'

spi = SPI(
    0,
    baudrate=40000000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))
print(spi) # prints parameters to the console display
print(text) # this script does not use the variable text even though it was assigned above, printed it here just because

# def loop_for_test():
display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.set_pos(0,0)
display.set_font(tt14)
display.set_color(color565(0, 0, 0), color565(255, 255, 255))

# note: background colour initally set in ili934xnew.py

def print_data():
    display.set_pos(150,0)
    display.set_font(tt32)
    display.set_color(color565(255, 255, 0), color565(255, 255, 255))
    display.print("Lelo's exercise")
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,30)
    display.set_font(tt24)
    display.print("Date:")
    display.set_pos(240,30)
    display.print("Time:")
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,55)
    display.print("2024, 10, 31")
    display.set_pos(240,55)
    display.print("23:00:")
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,80)
    display.print("session number")
    display.set_pos(240,80)
    display.print("session distance:")
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,105)
    display.print("6")    
    display.set_pos(240,105)
    display.print("1.5 km:")
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,130)
    display.print("Sessions today:")
    display.set_pos(240,130)
    display.print("Distance today:")
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,155)
    display.print("5:")
    display.set_pos(240,155)
    display.print("10 km:")
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0,180)
    display.print("speed now:")
    display.set_pos(240,180)
    display.print("average speed today:")
    display.set_color(color565(255, 0, 255), color565(255, 255, 255))
    display.set_pos(0,205)
    display.print("5 kph:")    
    display.set_pos(240,205)
    display.print("4 kph:")    

    time.sleep(5)


while True:
    
#    while repeat_loop == 0:
    print_data()