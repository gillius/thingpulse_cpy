import board
import busio
import adafruit_focaltouch
from micropython import const

i2c = busio.I2C(scl=board.IO22, sda=board.IO23)
ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False)

_TS_X_MAX = const(319)
_TS_Y_MAX = const(479)
_TS_ORIENT = const(3) # Update this based on your screen's orientation: 0, 1, 2 or 3 (0, 90, 180, 270 degrees)
def convert_touch(x: int, y: int) -> tuple:
    if _TS_ORIENT == 0:
        return (x, y)
    elif _TS_ORIENT == 1:
        return (y, _TS_X_MAX - x)
    elif _TS_ORIENT == 2:
        return (_TS_X_MAX - x, _TS_Y_MAX - y)
    else:
        return (_TS_Y_MAX - y, x)

def get_touch(scale: int = 1) -> tuple | None:
    try:
        if ft.touched:
            touches = ft.touches
            if touches:
                touch = touches[0]
                translated = convert_touch(touch['x'], touch['y'])
                return (translated[0] // scale, translated[1] // scale)
    except RuntimeError: # workaround https://github.com/adafruit/Adafruit_CircuitPython_FocalTouch/issues/28
        pass
    
    return None
