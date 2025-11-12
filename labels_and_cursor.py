from touch import get_touch

import ili9488
import displayio
import terminalio
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_display_shapes.triangle import Triangle

display = ili9488.make_display()

labels = []

def make_scrolling_label(text: str, x: int, y: int, **kwargs) -> ScrollingLabel:
    ret = ScrollingLabel(terminalio.FONT, text=text, max_characters=20, animate_time=0.3, **kwargs)
    ret.x = x
    ret.y = y
    labels.append(ret)
    return ret

root=displayio.Group()
root.scale=2
root.append(make_scrolling_label("RED Hello world CircuitPython scrolling label", 10, 10, color=0xFF0000))
root.append(make_scrolling_label("A second GREEN label is here!!!", 10, 50, color=0x00FF00))
root.append(make_scrolling_label("Lastly, a BLUE label is here!!!", 10, 100, color=0x0000FF))

cursor = Triangle(0, 0, 16, 0, 0, 16, fill=0x333333, outline=0x999999)
root.append(cursor)

display.root_group = root

while True:
    touch = get_touch(root.scale)
    if touch:
        cursor.x, cursor.y = touch

    for i in labels:
        i.update()
    
    display.refresh()
