from machine import Pin, Timer
import time

# --- CONFIGURE PINS ---
start_pin = Pin(16, Pin.IN, Pin.PULL_UP)   # START sensor
finish_pin = Pin(0, Pin.IN, Pin.PULL_UP)  # FINISH sensor

# --- STATE VARIABLES ---
start_time = None
finish_time = None
running = False

# --- CALLBACKS ---
def start_trigger(pin):
    global start_time, running
    if not running:  # Only start if not already running
        start_time = time.ticks_us()  # microsecond accuracy
        running = True
        print("\n Sprint started!")

def finish_trigger(pin):
    global start_time, finish_time, running
    if running:  # Only stop if timer is running
        finish_time = time.ticks_us()
        running = False
        
        elapsed_us = time.ticks_diff(finish_time, start_time)
        elapsed_s = elapsed_us / 1_000_000
        
        print("🏁 Sprint finished!")
        print(f"⏱️ Time: {elapsed_s:.3f} seconds\n")

# --- INTERRUPTS ---
start_pin.irq(trigger=Pin.IRQ_FALLING, handler=start_trigger)
finish_pin.irq(trigger=Pin.IRQ_FALLING, handler=finish_trigger)

print("System ready.\nWaiting for sensors...")

while True:
    pass
