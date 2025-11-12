# ILI9488 display initialization for ThingPulse Color Kit Grande

import board
import busio
import fourwire
import busdisplay
import displayio

# Started with data from https://github.com/Bodmer/TFT_eSPI/blob/master/TFT_Drivers/ILI9488_Init.h then modified based on datasheet https://www.lcdwiki.com/res/MSP3520/ILI9488%20Data%20Sheet.pdf
_INIT_SEQUENCE = (
    b"\xE0\x0F\x00\x03\x09\x08\x16\x0A\x3F\x78\x4C\x09\x0A\x08\x16\x1A\x0F" # Positive Gamma
    b"\xE1\x0F\x00\x16\x19\x03\x0F\x05\x32\x45\x46\x04\x0E\x0D\x35\x37\x0F" # Negative Gamma
    b"\xC0\x02\x17\x15" # Power Control 1
    b"\xC1\x01\x41"     # Power Control 2
    b"\xC5\x03\x00\x12\x80" # VCOM Control
    b"\x36\x01\xA0"     # Memory Access Control (flips X or Y or rows/cols, BGR vs RGB). 00 normal, 60 90 deg, C0 180 deg, A0 270 deg
    b"\x3A\x01\x66"     # Pixel Interface Format: 0x55 for 16-bit (not supported on SPI), 0x66 for 18-bit (1 byte per color ignoring low 2 bits)
    b"\xB0\x01\x00"     # Interface Mode Control
    b"\xB1\x01\xA0"     # Frame Rate Control -- this is supposed to take 2 parameters? This sets 60.76 or 58.35hz based on tearing effect line setting
    b"\xB4\x01\x02"     # Display Inversion Control : 2 = 2-dot inversion, 1 = 1-dot inversion, 0 = column inversion
    b"\xB6\x02\x00\x20" # Display Function Control : swap source scan sequence to right to left
    # b"\xB6\x03\x02\x02\x3B" # Display Function Control from TFT_eSPI
    b"\xB7\x01\x06"     # Entry Mode Set
    b"\xF7\x04\xA9\x51\x2C\x82" # Adjust Control 3
    b"\x11\x00"         # Exit Sleep
    b"\x29\x00"         # Display on
)

def make_display() -> ILI9488:
    print("Releasing display and configuring SPI")
    displayio.release_displays()

    # Per https://github.com/ThingPulse/esp32-weather-station-touch/blob/master/platformio.ini
    # MISO pin 19, MOSI 18, SCLK 5. CS=15, DC=2, RST=4.  BL (backlight) is 32. Touch CS=21
    spi = busio.SPI(clock=board.IO5, MISO=board.IO19, MOSI=board.IO18)
    if spi.try_lock():
        spi.configure(baudrate=27000000)
        spi.unlock()
    else:
        print("Unable to lock SPI to increase frequency!")
    print(f"SPI configured at {spi.frequency}hz")

    bus = fourwire.FourWire(spi, chip_select=board.IO15, command=board.IO2, reset=board.IO4, baudrate=spi.frequency)

    # width=480, height=320 for rotations A0 and 60, swapped for rotations 00 and C0
    return busdisplay.BusDisplay(bus, _INIT_SEQUENCE, color_depth=24, width=480, height=320, backlight_pin=board.IO32, auto_refresh=False)
