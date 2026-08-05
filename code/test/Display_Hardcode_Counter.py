from machine import I2C, Pin
from time import sleep
from i2c_lcd import I2cLcd

# I2C configuration
I2C_ADDR = 0x27      # from scan result [39]
I2C_ROWS = 4
I2C_COLS = 20

i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_ROWS, I2C_COLS)

lcd.clear()
lcd.putstr("Sprint Timer Test")

counter = 0

while counter < 70:
    lcd.move_to(0, 1)
    lcd.putstr("Counter: {:6d}".format(counter))
    counter += 1
    sleep(1)
