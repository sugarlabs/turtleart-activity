import os
import subprocess
cwd = os.getcwd()

# check if the system is Raspberry Pi, if not, raise exception
# Eg. output: Raspberry Pi 5 Model B Rev 1.0
try:
    with open('/sys/firmware/devicetree/base/model', 'r') as file:
        info = file.read()
        if "Raspberry" in info:
            is_rpi = True
        else:
            raise
except Exception:  # file not found
    raise  # change to None if on a PC


# check if requirements are met
req_met = True
with open(cwd + '/plugins/rpi/req.txt', 'r') as file:
    req_list = file.read().split("\n")
installed_modules = os.popen("pip freeze").read()

for req in req_list:
    if (req not in installed_modules):
        req_met = False


# to install req. - called from rpi.py
def install_req():
    subprocess.Popen(['pip', 'install', '--break-system-packages', '-r',
                      cwd + '/plugins/rpi/req.txt'])
    # todo: send notif to restart after a minute
    # todo: send notif if no internet

    # configure i2c, spi, etc comms
    os.system('''sudo raspi-config nonint do_i2c 0 &&
            sudo raspi-config nonintdo_spi 0 &&
            sudo raspi-config nonint do_serial_hw 0 &&
            sudo raspi-config nonint do_ssh 0 &&
            sudo raspi-config nonint do_camera 0 &&
            sudo raspi-config nonint disable_raspi_config_at_boot 0''')


# -- Add this line to config.txt to increase the speed of i2c devices -- #
# os.system("""sudo sed -i '$ a\dtparam=i2c_baudrate=1000000'
#               /boot/firmware/config.txt""")
