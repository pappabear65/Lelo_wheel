import machine
import time
import _thread

# Define GPIO pins for buttons
reed_speed = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)
reed_direction = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_DOWN)

reed_speedpwr = machine.Pin(19, machine.Pin.OUT)
reed_speedpwr.value(1)
reed_directionpwr = machine.Pin(20, machine.Pin.OUT)
reed_directionpwr.value(1)

power_lamp = machine.Pin(15, machine.Pin.OUT)
power_lamp.value(1)

def reed_speed_callback(pin):
#    print("speed trigger")
    power_lamp.value(1)
    
def reed_direction_callback(pin):
#    print("direction trigger")
    power_lamp.value(0)

reed_direction.irq(trigger=machine.Pin.IRQ_RISING, handler=reed_direction_callback)
print("IRQ reed_direction set:")

reed_speed.irq(trigger=machine.Pin.IRQ_RISING, handler=reed_speed_callback)
print("IRQ reed_speed set:")

# Main loop
while True:
    machine.idle()  # Keep the program running