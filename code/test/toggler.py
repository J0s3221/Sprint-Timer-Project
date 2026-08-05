from machine import Pin

led = Pin(25, Pin.OUT)  # onboard LED on classic Pico

led.toggle()
    

