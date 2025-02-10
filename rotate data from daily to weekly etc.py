import machine
import time
import os

# Initialize pins for switches
speed_switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
direction_switch = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Variables to track wheel rotations and direction
rotation_count = 0
direction = "CW"  # CW: clockwise, CCW: counter-clockwise
last_speed_time = time.ticks_ms()
last_direction_time = time.ticks_ms()
speed = 0
distance = 0
wheel_circumference = 1.0  # Replace with actual circumference

# File paths
daily_file = "/daily_log.txt"
weekly_file = "/weekly_log.txt"
monthly_file = "/monthly_log.txt"
yearly_file = "/yearly_log.txt"

# Interrupt handlers
def handle_speed(pin):
    global rotation_count, last_speed_time, speed, last_direction_time, direction
    current_time = time.ticks_ms()
    time_diff = time.ticks_diff(current_time, last_speed_time)
    rotation_count += 1
    speed = calculate_speed(time_diff)
    last_speed_time = current_time
    
    if time.ticks_diff(current_time, last_direction_time) > 0:
        direction = "CW"
    else:
        direction = "CCW"
    
    log_data()

def handle_direction(pin):
    global last_direction_time
    last_direction_time = time.ticks_ms()

def calculate_speed(time_diff):
    # Calculate speed based on time difference between rotations
    # Assuming wheel circumference in meters and time_diff in milliseconds
    return (wheel_circumference / (time_diff / 1000.0))  # Speed in meters per second

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
            if os.path.exists(yearly_file):
                os.remove(yearly_file)
            os.rename(monthly_file, yearly_file)
            open(monthly_file, 'w').close()
        if time.localtime()[6] == 0:  # First day of the week (Sunday)
            if os.path.exists(monthly_file):
                os.remove(monthly_file)
            os.rename(weekly_file, monthly_file)
            open(weekly_file, 'w').close()
        if os.path.exists(weekly_file):
            os.remove(weekly_file)
        os.rename(daily_file, weekly_file)
        open(daily_file, 'w').close()

# Attach interrupts to switches
speed_switch.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_speed)
direction_switch.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_direction)

# Main loop
while True:
    rotate_logs()
    time.sleep(60)  # Check every minute to rotate logs if needed