from machine import I2C, Pin

i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)

print("I2C scan:", i2c.scan())
