from machine import Pin
import time

def sensor_trigger(pin):
    print("Sensor triggered!")

sensor = Pin(16, Pin.IN, Pin.PULL_UP)
sensor.irq(trigger=Pin.IRQ_FALLING, handler=sensor_trigger)

while True:
    pass  # Main loop can do other things
