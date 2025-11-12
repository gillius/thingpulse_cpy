#Halloween scrolling demo app with 67 meme easter egg when you click the sides

from micropython import const
from touch import get_touch

import time
import ili9488
import displayio
import terminalio
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_display_shapes.triangle import Triangle

display = ili9488.make_display()

_width = const(480)
_mid_x = const(_width//2)
_height = const(320)
_mid_y = const(_height//2)

class Screen:
    def __init__(self):
        self.group = displayio.Group()
        self.labels = []

    def show(self):
        display.root_group = self.group

    def update(self):
        for i in self.labels:
            i.update()

    def make_scrolling_label(self, text: str, x: int, y: int, **kwargs) -> ScrollingLabel:
        ret = ScrollingLabel(terminalio.FONT, text=text, max_characters=15, animate_time=0.2, **kwargs)
        ret.x = x
        ret.y = y
        self.labels.append(ret)
        self.group.append(ret)
        return ret

main = Screen()
main.group.scale=6
main.make_scrolling_label("Happy Halloween!!!    ", 0, _height//2//main.group.scale, color=0xFF0000)

six = Screen()
six.group.scale=16
six.make_scrolling_label("6", _width//2//six.group.scale, _height//2//six.group.scale, color=0x00FF00, anchor_point=(0.5, 0.5))

seven = Screen()
seven.group.scale=16
seven.make_scrolling_label("7", _width//2//seven.group.scale, _height//2//seven.group.scale, color=0x0000FF, anchor_point=(0.5, 0.5))

screens = [main, six, seven]
num_screens = len(screens)

csi = 0
current_screen = screens[csi]
current_screen.show()

while True:
    touch = get_touch()
    if touch:
        if touch[0] > _mid_x:
            csi += 1
        else:
            csi -= 1

        if csi < 0:
            csi = num_screens - 1
        else:
            csi %= num_screens
            
        current_screen = screens[csi]
        current_screen.show()
        # time.sleep(0.25)

    current_screen.update()
    display.refresh()
