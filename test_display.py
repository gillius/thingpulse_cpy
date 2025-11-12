import ili9488
import displayio
import time

display = ili9488.make_display()

splash = displayio.Group()

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFF0000

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)
display.root_group = splash
display.refresh()
time.sleep(10)
