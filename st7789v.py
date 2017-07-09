import ustruct
from rgb import DisplaySPI, color565


class ST7789V(DisplaySPI):
    _COLUMN_SET = 0x2a
    _PAGE_SET = 0x2b
    _RAM_WRITE = 0x2c
    _RAM_READ = 0x2e
    _INIT = (
        (0x36, b'\x60'),
        (0x3a, b'\x55'), # Pixel Format
        (0xb2, b'\x0c\x0c\x00\x33\x33'),
        (0xb7, b'\x35'),
        (0xbb, b'\x2B'),
        (0xc0, b'\x2c'),
        (0xc2, b'\x01\xff'),
        (0xc3, b'\x11'),
        (0xc4, b'\x20'),
        (0xc6, b'\x0f'),
        (0xd0, b'\xa4\xa1'),
        (0xe0, # Set Gamma
        b'\xD0\x00\x05\x0E\x15\x0D\x37\x43\x47\x09\x15\x12\x16\x19')
        (0xe1, # Set Gamma
        b'\xD0\x00\x05\x0D\x0C\x06\x2D\x44\x40\x0E\x1C\x18\x16\x19')
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    def __init__(self, spi, dc, cs, rst=None, width=240, height=320):
        super().__init__(spi, dc, cs, rst, width, height)
        self._scroll = 0

    def scroll(self, dy=None):
        if dy is None:
            return self._scroll
        self._scroll = (self._scroll + dy) % self.height
        self._write(0x37, ustruct.pack('>H', self._scroll))

    def init(self):
        for command, data in self._INIT:
            self._write(command, data)

        for command, data in (
            (0x11, None), # Exit sleep
            (0x29, None) # Display on
        ):
            self._write(command, data)
            utime.sleep_ms(10)

#    def reset(self):
#        self.rst(1)
#        utime.sleep_ms(10)
#        self.rst(0)
#        utime.sleep_ms(20)
#        self.rst(1)
#        utime.sleep_ms(20)
