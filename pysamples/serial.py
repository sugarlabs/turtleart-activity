# Copyright (c) 2010-11, Walter Bender, Tony Forster
#
# This Python block writes serial output to a USB port and pushes
# serial input to the heap.
#
# To use this block:
#    (1) import this file into a Python Block;
#    (2) pass text strings as an argument
#    (3) use a Pop Block to retrieve any strings input from serial device.


def myblock(tw, args):  # x is the string to transmit
    import serial  # you may need to install this library

    # serial device on USB, 9600 baud
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    ser.write(str(args[0]))  # send string x
    st = ser.read(1000)  # read up to 1000 bytes
    tw.lc.heap.append(st)  # append to heap
    ser.close()
