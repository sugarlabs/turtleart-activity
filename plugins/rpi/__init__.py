# check if the system is Raspberry Pi, if not, return
# Eg. output: Raspberry Pi 5 Model B Rev 1.0
try:
    with open('/sys/firmware/devicetree/base/model', 'r') as file:
        info = file.read()
        if "Raspberry" not in info:
            raise
except: # file not found
    None


#--- Have to do this when setting up RPi to enable spi & i2c interfaces ---#
# os.system("sudo raspi-config nonint do_i2c 0 && sudo raspi-config nonint\
# do_spi 0 && sudo raspi-config nonint do_serial_hw 0 && sudo raspi-config\
# nonint do_ssh 0 && sudo raspi-config nonint do_camera 0 && sudo raspi-config\
# nonint disable_raspi_config_at_boot 0")

#--- Also add this line to config.txt to increase the speed of the display ---#
# os.system("sudo sed -i '$ a\dtparam=i2c_baudrate=1000000'\
# /boot/firmware/config.txt)
