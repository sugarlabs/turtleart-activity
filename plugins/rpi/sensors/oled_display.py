import sys
import time
import board
import displayio
from i2cdisplaybus import I2CDisplayBus
from fourwire import FourWire
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306


def main(width, height, text_color, text):
    height = int(height)
    width = int(width)
    text_color = int(text_color)
    displayio.release_displays()
    oled_reset = board.D27

    # Use for I2C
    i2c = board.I2C()
    display_bus = I2CDisplayBus(i2c, device_address=0x3C, reset=oled_reset)

    # Use for SPI
    # spi = board.SPI()
    # oled_cs = board.D5
    # oled_dc = board.D6
    # display_bus = FourWire(spi, command=oled_dc, chip_select=oled_cs,
    #                               reset=oled_reset, baudrate=1000000)
    display = adafruit_displayio_ssd1306.SSD1306(
        display_bus, width=width, height=height
    )
    splash = displayio.Group()
    display.root_group = splash

    # clear oled
    color_bitmap = displayio.Bitmap(width, height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF if text_color == 0 else 0x000000
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,
                                   x=0, y=0)
    splash.append(bg_sprite)

    # print on oled
    if text != "":
        if len(text) > 20:
            text = text[:20]
        text_area = label.Label(
            terminalio.FONT,
            text=text,
            color=0x000000 if text_color == 0 else 0xFFFFFF,
            x=5,
            y=5,
        )
        splash.append(text_area)
    time.sleep(0.2)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
