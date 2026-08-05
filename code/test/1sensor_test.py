from machine import Pin
import time

# Change the pin number to the one you’re using
sensor = Pin(16, Pin.IN, Pin.PULL_UP)

print("Testing sensor input...")

while True:
    value = sensor.value()
    print("GPIO:", value)
    time.sleep(0.5)
