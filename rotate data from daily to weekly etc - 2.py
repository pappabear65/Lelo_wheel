#cgpt example for ideas

import machine
import time
import os

# Initialize pins for switches
switch_speed = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
switch_direction = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Variables to track wheel rotations and direction
rotation_count = 0
direction = 0  # 0: forward, 1: backward
last_time = time.ticks_ms()
speed = 0
distance = 0

# File paths
daily_file = "/daily_log.txt"
weekly_file = "/weekly_log.txt"
monthly_file = "/monthly_log.txt"
yearly_file = "/yearly_log.txt"

# Interrupt handlers
def handle_speed(pin):
    global rotation_count, last_time, speed
    current_time = time.ticks_ms()
    rotation_count += 1
    speed = calculate_speed(current_time - last_time)
    last_time = current_time
    log_data()

def handle_direction(pin):
    global direction
    direction = 1 if direction == 0 else 0

def calculate_speed(time_diff):
    # Calculate speed based on time difference between rotations
    # Assuming wheel circumference and time_diff in milliseconds
    return (wheel_circumference / time_diff) * 1000

def calculate_distance(rotations):
    # Calculate distance based on the number of rotations
    return rotations * wheel_circumference

def log_data():
    global rotation_count, direction, speed, distance
    distance = calculate_distance(rotation_count)
    data = f"{time.time()},{rotation_count},{direction},{speed},{distance}\n"
    with open(daily_file, 'a') as f:
        f.write(data)

def rotate_logs():
    # Rotate logs from daily to weekly, monthly, and yearly
    if time.localtime()[3] == 0:  # If the hour is 0, rotate logs
        if time.localtime()[2] == 1:  # First day of the month
            os.rename(monthly_file, yearly_file)
            open(monthly_file, 'w').close()
        if time.localtime()[6] == 0:  # First day of the week (Sunday)
            os.rename(weekly_file, monthly_file)
            open(weekly_file, 'w').close()
        os.rename(daily_file, weekly_file)
        open(daily_file, 'w').close()

# Attach interrupts to switches
switch_speed.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_speed)
switch_direction.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_direction)

# Main loop
while True:
    rotate_logs()
    time.sleep(60)  # Check every minute to rotate logs if needed
