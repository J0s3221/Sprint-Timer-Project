# lcd_api.py
class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0


    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]

        if row >= self.num_lines:
            row = self.num_lines - 1
        if col >= self.num_columns:
            col = self.num_columns - 1

        self.cursor_x = col
        self.cursor_y = row
        self.hal_write_command(0x80 | (row_offsets[row] + col))


    def putstr(self, string):
        for char in string:
            self.hal_write_data(ord(char))
