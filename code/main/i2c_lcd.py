# i2c_lcd.py
from lcd_api import LcdApi
from time import sleep_ms
class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 0x08 sleep_ms(20)
        self.hal_write_command(0x33)
        self.hal_write_command(0x32)
        self.hal_write_command(0x28)
        self.hal_write_command(0x0C)
        self.hal_write_command(0x06)
        self.clear()
        super().__init__(num_lines, num_columns)
    
    def hal_write_command(self, cmd):
        self._write_byte(cmd, 0)
    
    def hal_write_data(self, data):
        self._write_byte(data, 1)
    
    def _write_byte(self, data, mode):
        high = data & 0xF0
        low = (data << 4) & 0xF0
        self._write(high | mode)
        self._write(low | mode)
    
    def _write(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight]))
        
        
        
        
        