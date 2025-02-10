import network
import ntptime
import time
import secrets

# WiFi credentials
SSID = secrets.network_secrets["ssid"]
PASSWORD = secrets.network_secrets["password"]

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    # Wait for the connection to establish
    while not wlan.isconnected():
        time.sleep(1)
    
    print('Connected to WiFi:', wlan.ifconfig())

# Function to sync NTP time
def sync_time():
    try:
        ntptime.settime()
        print("Time synchronized with NTP.")
    except Exception as e:
        print("Error syncing time:", e)

# Main loop
def main():
    connect_wifi()  # Connect to WiFi
    
    last_sync_time = time.time()  # Store the time of the last sync
    sync_interval = 21600  # Sync every 6 hours (in seconds)
    
    while True:
        current_time = time.time()
        
        # Check if it's time to sync
        if current_time - last_sync_time >= sync_interval:
            sync_time()  # Sync time
            last_sync_time = current_time  # Update last sync time
        
        # Continue doing other tasks in your script
        print("Running other tasks...")
        
        # Sleep for a while before checking again (to avoid busy-waiting)
        time.sleep(10)  # Adjust this as needed (e.g., 10 seconds)

if __name__ == '__main__':
    main()
