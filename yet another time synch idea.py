# Import necessary modules
import time
import network

# Set global variables or configurations
SSID = "your-SSID"
PASSWORD = "your-PASSWORD"
LED_PIN = 15  # Example pin for an LED

# Define any helper functions
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    
    print("Connected to WiFi:", wlan.ifconfig())

def blink_led():
    from machine import Pin
    led = Pin(LED_PIN, Pin.OUT)
    
    # Blink LED every second
    while True:
        led.value(not led.value())  # Toggle the LED
        time.sleep(1)

# Define the main function that controls the program flow
def main():
    print("Starting script...")
    
    # Connect to WiFi
    connect_wifi()

    # Perform other tasks, for example, blink an LED
    blink_led()

# If the script is executed directly, call the main function
if __name__ == "__main__":
    main()
