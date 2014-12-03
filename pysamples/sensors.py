# Copyright (c) 2010-11, Walter Bender, Tony Forster
#
# This Python block returns with the brightness sensor value in the heap
# a range of parameters can be measured, for example, substitute any of
# these strings for the string in the program below.
#
# /sys/devices/platform/olpc-battery.0/power_supply/olpc-battery/current_now
# /sys/devices/platform/olpc-battery.0/power_supply/olpc-battery/voltage_now
# /sys/devices/platform/dcon/backlight/dcon-bl/actual_brightness


def myblock(tw, x):  # ignores second argument
    import os

    # The light sensor is only available on the XO 1.75
    device = '/sys/devices/platform/olpc-ols.0/level'

    if os.path.exists(device):
        fh = open(device)
        string = fh.read()
        fh.close()
        tw.lc.heap.append(float(string))  # append as a float value to the heap
    else:
        tw.lc.heap.append(-1)

# If you can work out how to use them...
# accelerometer: /dev/input/event0 ???
# power button: /dev/input/event1
# lid switch: /dev/input/event2
# ebook: /dev/input/event3
# headphone jack: /dev/input/event7
# microphone jack: /dev/input/event8
# rotate, cursor, and game pad keys: /dev/input/event10
