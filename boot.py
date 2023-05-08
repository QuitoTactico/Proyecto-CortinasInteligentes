#############################################
# Provide your Wifi connection details here #
#############################################

WIFI_SSID = "Claro140"
WIFI_PASSWORD = "Magivi0917"

#############################################

import network
from time import sleep
from machine import Pin
import ntptime

sleep(1) # Without this, the USB handshake seems to break this script and then fail sometimes.

led = Pin("LED", Pin.OUT, value=1)

wlan = None
while not wlan or wlan.status() != 3:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Blink LED slowly until the Wifi is connected.

    while True:
        print(wlan)
        led.toggle()
        sleep(0.2)
        if wlan.status() in [-1, -2, 3]:
            break

# Set the RTC to the current time

ntptime.settime()

# Solid LED means we're connected and ready to go
led.on()
print(wlan)

