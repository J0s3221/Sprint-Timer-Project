from machine import Pin, I2C
from time import sleep, ticks_us, ticks_diff
from i2c_lcd import I2cLcd
from machine import ADC

#===== Battery percentage ====
battery_adc = ADC(26)  # GP26

# ===== LCD SETUP =====
# I2C configuration
I2C_ADDR = 0x27      # from scan result [39]
I2C_ROWS = 4
I2C_COLS = 20

i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_ROWS, I2C_COLS)

# ===== SENSOR SETUP =====
start_sensor = Pin(16, Pin.IN, Pin.PULL_UP)
stop_sensor  = Pin(4, Pin.IN, Pin.PULL_UP)

# ===== STATE =====
last_time_1 = None
last_time_2 = None

# ===== HELPER FUNCTIONS =====
def show_last_time():
    if last_time_1 is None:
        lcd.move_to(0, 2)
        lcd.putstr("Last 1: --- s ")
    else:
        lcd.move_to(0, 2)
        lcd.putstr("Last 1: {:.3f} s ".format(last_time_1))
    
    if last_time_2 is None:
        lcd.move_to(0, 3)
        lcd.putstr("Last 2: --- s ")
    else:
        lcd.move_to(0, 3)
        lcd.putstr("Last 2: {:.3f} s ".format(last_time_2))

def show_ready():
    lcd.clear()
    sleep(0.05)
    
    batt = get_battery_percent()
    lcd.putstr("SPRINT TIMER   {:>3}%".format(batt))
    print("Battery %:", batt)
    
    lcd.move_to(0, 1)
    lcd.putstr("READY               ")
    show_last_time()

def show_running():
    sleep(0.02)

    batt = get_battery_percent()
    lcd.move_to(0, 0)
    lcd.putstr("SPRINT TIMER {:>3}%".format(batt))

    lcd.move_to(0, 1)
    lcd.putstr("RUNNING...           ")
    show_last_time()

def show_result(seconds):
    global last_time_1
    global last_time_2

    lcd.clear()
    sleep(0.05)
    lcd.putstr("TIME:")
    lcd.move_to(0, 1)
    lcd.putstr("{:.3f} s            ".format(seconds))
    show_last_time()
    last_time_2 = last_time_1
    last_time_1 = seconds
    
def mininum_time(seconds):
    # if its below the world record I'll call Usain Bolt for you and you guys can talk
    if seconds < 4.21:
        return 0
    # if its above the world record return 1
    return 1

def show_below_min_err():
    lcd.clear()
    sleep(0.05)
    lcd.putstr("     WARNING:")
    lcd.move_to(0, 2)
    lcd.putstr("  BELOW THE WORLD")
    lcd.move_to(0, 3)
    lcd.putstr("     RECORD!")

lcd.clear()
sleep(2)
lcd.putstr("    Sprint Timer")
lcd.move_to(0, 1)
lcd.putstr("      LCD OK")
sleep(5)

def read_battery_voltage():
    raw = battery_adc.read_u16()
    voltage_adc = (raw / 65535) * 3.3  # ADC voltage (0–3.3V)

    voltage_battery = voltage_adc * 2  # because of divider (100k/100k)

    return voltage_battery

def battery_percentage(voltage):
    min_v = 6.0
    max_v = 8.4

    percent = (voltage - min_v) / (max_v - min_v) * 100

    if percent > 100:
        percent = 100
    if percent < 0:
        percent = 0

    return int(percent)

def get_battery_percent():
    v = read_battery_voltage()
    return battery_percentage(v)

# ===== MAIN LOOP =====
show_ready()

while True:

    # Wait for start sensor
    while start_sensor.value() == 0:
        sleep(0.001)

    print("\n sensor activated show running!")
    start_time = ticks_us()
    show_running()

    # Wait for stop sensor
    while stop_sensor.value() == 0:
        sleep(0.001)

    print("\n sensor activated, stop running show finish!")
    end_time = ticks_us()

    elapsed_us = ticks_diff(end_time, start_time)
    elapsed_s = elapsed_us / 1_000_000

    if mininum_time(elapsed_s) == 1:
        print(f"\n {elapsed_s:.3f}")
        show_result(elapsed_s)
    else:
        print("Hello Usain Bolt! I don't think you should be here :)")
        show_below_min_err()

    # Wait before next run
    sleep(5)
    show_ready()
