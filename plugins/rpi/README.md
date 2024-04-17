# RPi Plugin

This plugin will leverage the pins of Raspberry Pi to attach and control several peripherals to it. This plugin uses the *adafruit_blinka* library to communicate with sensors and components. Combining them with turtle blocks makes things as simple as they can get.

This plugin is compatible not only with Raspberry Pi but also with several other linux SBCs; OrangePi, BeagleBone, Google Coral Dev Boad, Jetson, Banana Pi, and NanoPi to name a few.

In Raspberry Pi, for using each component/sensor you will have to enter the pin number they are connected to with a 'D' in front of them. For example, **D7** for **GPIO 7** as you can see in the pinout diagram (of RPi 4/5) below.\
Note that GPIO numbers and pin numbers (in the circle) are different. We need the GPIO numbers.


![RPi 5 pinout](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png)


Run this for first-time installation to set up I2C, SPI, and a few other configurations.
```
sudo raspi-config nonint do_i2c 0 && sudo raspi-config nonint do_spi 0 && sudo raspi-config nonint do_serial_hw 0 && sudo raspi-config nonint do_ssh 0 && sudo raspi-config nonint do_camera 0 && sudo raspi-config nonint disable_raspi_config_at_boot 0
```

# For developers
Improvements and additions are very much welcomed.

Structure:

```
rpi
├── rpi.py
├── functions.py
├── libs
│   └── //dependencies//
├── sensors
│   ├── add_path.py
│   └── //other sensor's scripts//
└── //some other files//

```

## Use sensors in your activities

Copy `functions.py`, `libs`, and `sensors` to your desired location. Update path in `sensors/add_path.py` 

All the functions to use sensors are listed under `functions.py`. You simply need to call the functions and enter the pin numbers (for example, "D7") as entered by the user as parameters.


## How to contribute
For adding more sensors/components you can add turtle blocks in `rpi.py`, their corresponding functions in `functions.py`, and libraries in the `libs` folder. Download the libraries from https://pypi.org and extract the built distributions (py3) into libs. Import `sensors/add_path.py` in all the functions. 

The pallet is only visible if the device is Raspberry Pi, so don't forget to disable the check-in `__init__.py`

# Screenshots

Oled Display:

<img src="https://github.com/44yu5h/turtleart-activity/blob/c2bc2357e806543c3d7a8b60a29ce8f7649e318b/plugins/rpi/screenshots/ta_oled.png?raw=true" height="300"> <img src="https://github.com/44yu5h/turtleart-activity/blob/c2bc2357e806543c3d7a8b60a29ce8f7649e318b/plugins/rpi/screenshots/oled.jpg?raw=true" height="300">


Push Button:

<img src="https://github.com/44yu5h/turtleart-activity/blob/c2bc2357e806543c3d7a8b60a29ce8f7649e318b/plugins/rpi/screenshots/ta_btn.png?raw=true" height="300"> <img src="https://github.com/44yu5h/turtleart-activity/blob/c2bc2357e806543c3d7a8b60a29ce8f7649e318b/plugins/rpi/screenshots/btn.gif?raw=true" height="300">