import time
import plugins.rpi.sensors.add_path
import os
import board
import digitalio
import adafruit_hcsr04
import subprocess
cwd=os.getcwd()
import logging
_logger = logging.getLogger('turtleart-activity RPi plugin') 


# Digital output
def digitalWrite(pin_no: str, val: float):
    if not hasattr(board,pin_no):
        return      # + send a message
    pin = digitalio.DigitalInOut(getattr(board,pin_no))
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = int(val)
# Digital input
def digitalRead(pin_no: str):
    if not hasattr(board,pin_no):
        return
    pin = digitalio.DigitalInOut(getattr(board,pin_no))
    pin.direction = digitalio.Direction.INPUT
    return bool(pin.value)

#delay
def delay(ms: int):
    time.sleep(ms/1000)

# Button
def btn(pin: str):
    button=0
    try:
        button = digitalio.DigitalInOut(getattr(board,pin))
        button.direction = digitalio.Direction.INPUT
    except:
        None
    button.pull = digitalio.Pull.UP
    return not button.value


# HC-SR04 Ultrasonic distance sensor
class _dist:
    def def_dist(self, trigger:str, echo:str):
        try:
            self.sonar = adafruit_hcsr04.HCSR04(\
trigger_pin = getattr(board,trigger), echo_pin=getattr(board,echo))
        except:
            return
    def dst(self):
        try:
            s=0.0
            for i in range(20):
                if (self.sonar.distance < 1):
                    i=i-1
                    continue
                s+=self.sonar.distance
            return round(s/20,1)
        except:
            return 0.0
dist=_dist()


# OLED display
class _oled():
    def define(self, _height, _width, _text_color):
        self.width = int(_width)
        self.height = int(_height)
        self.text_color = int(_text_color)
    def print(self, text):
        subprocess.Popen('python3 '+cwd+'/plugins/rpi/sensors/oled_display.py '
                         +str(self.height)+' '+str(self.width)+' '+
                         str(self.text_color)+' '+str(text), shell=True)
oled=_oled()
