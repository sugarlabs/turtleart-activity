# -*- coding: utf-8 -*-
#Copyright (c) 2011 Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

from gettext import gettext as _

'''
Note: this file contains string from plugins and related projects that
are not included in the default packaaging of Turtle Art. The reason
for gathering these strings here is to enable us to use one common POT
file across all of these projects.

TODO: build some automated way of maintaining this file.
'''

# ACTIVITIES

TURTLEARTMINI_STRINGS = [
    _('Turtle Art Mini')
    ]

TURTLECONFUSION_STRINGS = [
    _('Turtle Confusion'),
    _('Select a challenge')
    ]

TURTLEAMAZONAS_STRINGS = [
    _('Amazonas Tortuga'),
    _('Select a challenge')
    ]

# PLUGINS

CURRENCY_STRINGS = [
    _('Palette of Mexican pesos'),
    _('Palette of Colombian pesos'),
    _('Palette of Rwandan francs'),
    _('Palette of US dollars'),
    _('Palette of Australian dollars'),
    _('Palette of Paraguayan Guaranies'),
    _('Palette of Peruvian Nuevo Soles'),
    _('Palette of Uruguayan Pesos')
    ]

BUTIA_STRINGS = [
    #TRANS: Butia is the Arduino Robot Project from Uruguay
    #(http://www.fing.edu.uy/inco/proyectos/butia/)
    _('TurtleBots'),
    _('adjust LED intensity between 0 and 255'),
    _('returns the object gray level as a number between 0 and 1023'),
    _('returns 1 when the button is press and 0 otherwise'),
    _('returns the ambient light level as a number between 0 and 1023'),
    _('returns the ambient temperature as a number between 0 and 255'),
    _('returns the distance from the object in front of the sensor as a number \
between 0 and 255'),
    _('returns 0 or 1 depending on the sensor inclination'),
    _('returns 1 when the sensors detects a magnetic field, 0 otherwise'),
    _('switches from 0 to 1, the frequency depends on the vibration'),
    _('returns the value of the resistance'),
    _('LED'),
    _('button'),
    _('grayscale'),
    _('ambient light'),
    _('temperature'),
    _('distance'),
    _('tilt'),
    _('magnetic induction'),
    _('vibration'),
    _('resistance'),
    _('Butia Robot'),
    _('refresh Butia'),
    _('refresh the state of the Butia palette and blocks'),
    #TRANS: This string is shorthand for "battery charge of Butia"
    _('battery charge Butia'),
    _('returns the battery charge as a number between 0 and 255'),
    #TRANS: This string is shorthand for "speed of Butia"
    _('speed Butia'),
    _('set the speed of the Butia motors as a value between 0 and 1023, \
passed by an argument'),
    #TRANS: This string is shorthand for "move Butia forward"
    _('forward Butia'),
    _('move the Butia robot forward'),
    _('move the Butia robot forward a predefined distance'),
    #TRANS: This string is shorthand for "turn Butia left"
    _('left Butia'),
    _('turn the Butia robot at left'),
    #TRANS: This string is shorthand for "move Butia backward"
    _('backward Butia'),
    _('move the Butia robot backward'),
    _('move the Butia robot backward a predefined distance'),
    #TRANS: This string is shorthand for "turn Butia right"
    _('right Butia'),
    _('turn the Butia robot at right'),
    _('turn Butia'),
    _('turn the Butia robot x degrees'),
    _('stop Butia'),
    _('stop the Butia robot'),
    _('Butia')
]

FOLLOWME_STRINGS = [
    _('Error importing Pygame. This plugin require Pygame 1.9'),
    _('Error on initialization of the camera'),
    _('No camera was found'),
    _('Error stopping camera'),
    _('Error starting camera'),
    #TRANS: The "mask" is used to restrict processing to a region in the image
    _('Error in get mask'),
    _('FollowMe'),
    _('refresh FollowMe'),
    _('Search for a connected camera.'),
    #TRANS: the calibration is used to match an RGB color to a target
    _('calibration'),
    _('store a personalized calibration'),
    _('return a personalized calibration'),
    _('follow'),
    _('follow a color or calibration'),
    _('brightness'),
    _('set the camera brightness as a value between 0 to 255.'),
    _('minimum pixels'),
    _('set the minimal number of pixels to follow'),
    _('threshold'),
    # TRANS: RGB color space (red, green, blue)
    _('set a threshold for a RGB color'),
    _('camera mode'),
    # TRANS: RGB, YUV, and HSV are color spaces
    _('set the color mode of the camera: RGB; YUV or HSV'),
    _('get brightness'),
    _('get the brightness of the ambient light'),
    _('average color'),
    _('if set to 0 then color averaging is off during calibration; for other values it is on'),
    _('x position'),
    _('return x position'),
    _('y position'),
    _('return y position'),
    _('pixels'),
    _('return the number of pixels of the biggest blob'),
    # TRANS: RGB color space (red, green, blue)
    _('set the color mode of the camera to RGB'),
    # TRANS: YUV color space (luminance, chrominance)
    _('set the color mode of the camera to YUV'),
    # TRANS: HSV color space (hue, saturation, value)
    _('set the color mode of the camera to HSV'),
    _('empty calibration'),
    _('error in string conversion')
]

SUMO_STRINGS = [
    #TRANS: SumBot is a robot programmed for "Sumo wrestling"
    _('SumBot'),
    _('speed SumBot'),
    _('submit the speed to the SumBot'),
    _('set the default speed for the movement commands'),
    #TRANS: This string is shorthand for "move SumBot forward"
    _('forward SumBot'),
    _('move SumBot forward'),
    #TRANS: This string is shorthand for "move SumBot backward"
    _('backward SumBot'),
    _('move SumBot backward'),
    _('stop SumBot'),
    _('stop the SumBot'),
    #TRANS: This string is shorthand for "turn SumBot left"
    _('left SumBot'),
    _('turn left the SumBot'),
    #TRANS: This string is shorthand for "move SumBot right"
    _('right SumBot'),
    _('turn right the SumBot'),
    #TRANS: The angle to the center is the angle SumBot must turn to
    #face the center of the playing field
    _('angle to center'),
    #TRANS: dohyo is the playing field
    _('get the angle to the center of the dohyo'),
    #TRANS: The angle to the center is the angle SumBot must turn to
    #face the Enemy (opponent)
    _('angle to Enemy'),
    _('get the angle to the Enemy'),
    #TRANS: This string is shorthand for "x coordinate of SumBot"
    _('x coor. SumBot'),
    _('get the x coordinate of the SumBot'),
    #TRANS: This string is shorthand for "y coordinate of SumBot"
    _('y coor. SumBot'),
    _('get the y coordinate of the SumBot'),
    #TRANS: This string is shorthand for "x coordinate of SumBot's enemy"
    _('x coor. Enemy'),
    _('get the x coordinate of the Enemy'),
    #TRANS: This string is shorthand for "y coordinate of SumBot's enemy"
    _('y coor. Enemy'),
    _('get the y coordinate of the Enemy'),
    #TRANS: This string is shorthand for "rotation of SumBot"
    _('rotation SumBot'),
    _('get the rotation of the Sumbot'),
    #TRANS: This string is shorthand for "rotation of SumBot's enemy"
    _('rotation Enemy'),
    _('get the rotation of the Enemy'),
    _('distance to center'),
    #TRANS: dohyo is the playing field
    _('get the distance to the center of the dohyo'),
    _('distance to Enemy'),
    _('get the distance to the Enemy'),
    _('update information'),
    _('update information from the server')
]

PHYSICS_STRINGS = [
    # TRANS: Please use similar terms to those used in the Physics Activity
    _('Palette of physics blocks'),
    _('start polygon'),
    _('Begin defining a new polygon based \
on the current Turtle xy position.'),
    _('add point'),
    _('Add a new point to the current \
polygon based on the current Turtle xy position.'),
    _('end polygon'),
    _('Define a new polygon.'),
    _('end filled polygon'),
    _('Not a simple polygon'),
    _('Define a new filled polygon.'),
    _('triangle'),
    # TRANS: base of a triangle
    _('base'),
    _('height'),
    _('Add a triangle object to the project.'),
    _('circle'),
    _('Add a circle object to the project.'),
    _('rectangle'),
    _('width'),
    _('height'),
    _('Add a rectangle object to the project.'),
    _('reset'),
    _('Reset the project; clear the object list.'),
    _('motor'),
    #TRANS: torque as in engine torque
    _('torque'),
    _('speed'),
    _('Motor torque and speed range from 0 (off) to positive numbers; \
motor is placed on the most recent object created.'),
    _('pin'),
    _('Pin an object down so that it cannot fall.'),
    _('joint'),
    _('x'),
    _('y'),
    _('Join two objects together (the most \
recent object created and the object at point x, y).'),
    _('save as Physics activity'),
    _('Save the project to the Journal as a Physics activity.'),
    # TRANS: Here, gear means a toothed wheel, as in a clock-works
    _('gear'),
    _('Add a gear object to the project.'),
    _('density'),
    _('Set the density property for objects \
(density can be any positive number).'),
    _('friction'),
    _('Set the friction property for objects (value from 0 to 1, \
where 0 turns friction off and 1 is strong friction).'),
    # TRANS: bounciness is coefficient of restitution
    _('bounciness'),
    _('Set the bounciness property for \
objects (a value from 0 to 1, where 0 means no bounce and 1 is very bouncy).'),
    # TRANS: dynamic here means moving vs in a fixed position
    _('dynamic'),
    _('If dynamic = 1, the object can move; \
if dynamic = 0, it is fixed in position.')
]

WEDO_STRINGS = [
    # TRANS: WeDo is a robotics product of the LEGO company
    _('Palette of WeDo blocks'),
    _('WeDo'),
    _('set current WeDo device'),
    _('number of WeDo devices'),
    _('tilt'),
    _('tilt sensor output: (-1 == no tilt,\
 0 == tilt forward, 3 == tilt back, 1 == tilt left, 2 == tilt right)'),
    _('distance'),
    #TRANS: This string is shorthand for "output of the distance sensor"
    _('distance sensor output'),
    _('Motor A'),
    _('returns the current value of Motor A'),
    _('Motor B'),
    _('returns the current value of Motor B'),
    _('set the value for Motor A'),
    _('set the value for Motor B'),
    _('WeDo is unavailable'),
    # TRANS: e.g., Wedo 2 is unavailable, defaulting to 1
    _('WeDo %d is unavailable; defaulting to 1'),
    # TRANS: %(device)s and %(wedo_number)d are substitution strings;
    # please leave untranslated
    _('%(device)s is unavailable on WeDo %(wedo_number)d')
]


LEGO_STRINGS = [
    # TRANS: Lego NXT is a robotics product of the LEGO company
    _('Palette of LEGO NXT blocks of motors'),
    _('Palette of LEGO NXT blocks of sensors'),
    # TRANS: touch sensor (implemented as a button)
    _('touch'),
    # TRANS: distance sensor (implemented using ultrasonics)
    _('ultrasonic'),
    _('color'),
    _('light'),
    _('sound'),
    _('grey'),
    # TRANS: The brick is the NXT controller
    _('Please check the connection with the brick'),
    _("Invalid port '%s'. Port must be: PORT A, B or C"),
    _("Invalid port '%s'. Port must be: PORT 1, 2, 3 or 4"),
    _('The value of power must be between -127 to 127'),
    _("The parameter must be a integer, not '%s'"),
    _('An error has occurred: check all connections and try to reconnect'),
    _('NXT found %s bricks'),
    _('NXT not found'),
    _('Brick number %s was not found'),
    _('refresh NXT'),
    _('Search for a connected NXT brick.'),
    _('NXT'),
    _('set current NXT device'),
    _('number of NXT devices'),
    _('brick name'),
    _('Get the name of a brick.'),
    _('play tone'),
    _('frequency'),
    _('time'),
    _('Play a tone at frequency for time.'),
    # TRANS: turn is the action
    _('turn motor\n\n'),
    _('port'),
    _('power'),
    # TRANS: rotations is quantity of turns
    _('rotations'),
    _('turn a motor'),
    _('synchronize\n\nmotors'),
    _('steering'),
    _('synchronize two motors connected in PORT B and PORT C'),
    _('PORT A'),
    _('PORT A of the brick'),
    _('PORT B'),
    _('PORT B of the brick'),
    _('PORT C'),
    _('PORT C of the brick'),
    _('start motor'),
    _('Run a motor forever.'),
    _('brake motor'),
    _('Stop a specified motor.'),
    # TRANS: reset is used to reset the counter associated with the motor
    _('reset motor'),
    _('Reset the motor counter.'),
    _('motor position'),
    _('Get the motor position.'),
    _('PORT 1'),
    _('PORT 1 of the brick'),
    _('read'),
    _('sensor'),
    _('Read sensor output.'),
    _('PORT 2'),
    _('PORT 2 of the brick'),
    _('light sensor'),
    _('grey sensor'),
    _('PORT 3'),
    _('PORT 3 of the brick'),
    _('touch sensor'),
    _('distance sensor'),
    _('PORT 4'),
    _('PORT 4 of the brick'),
    _('sound sensor'),
    _('color sensor'),
    # TRANS: set light is used to set the light level associated with
    # the color sensor (which can emit light as well as sense it)
    _('set light'),
    _('Set color sensor light.'),
    # TRANS: the battery level is the charge level of the brick
    _('battery level'),
    _('Get battery level of the brick')
]

ARDUINO_STRINGS = [
    #TRANS: Arduino plugin to control an Arduino board
    _('HIGH'),
    _('LOW'),
    _('INPUT'),
    _('OUTPUT'),
    #TRANS: PWM is pulse-width modulation
    _('PWM'),
    _('SERVO'),
    _('ERROR: Check the Arduino and the number of port.'),
    _('ERROR: Value must be a number from 0 to 255.'),
    _('ERROR: Value must be either HIGH or LOW.'),
    _('ERROR: The mode must be either INPUT, OUTPUT, PWM or SERVO.'),
    _('refresh Arduino'),
    _('Search for connected Arduinos.'),
    _('Arduino'),
    _('set current Arduino board'),
    _('number of Arduinos'),
    _('number of Arduino boards'),
    _('Arduino name'),
    _('Get the name of an Arduino.'),
    #TRANS: pin mode is used to specify the mode (INPUT, OUTPUT, etc)
    #in which an I/O pin is being used.
    _('pin mode'),
    _('pin'),
    _('mode'),
    _('Select the pin function (INPUT, OUTPUT, PWM, SERVO).'),
    _('analog write'),
    _('value'),
    _('Write analog value in specified port.'),
    _('analog read'),
    _('Read value from analog port. Value may be between 0 and 1023. Use Vref \
to determine voltage. For USB, volt=((read)*5)/1024) approximately.'),
    _('digital write'),
    _('Write digital value to specified port.'),
    _('digital read'),
    _('Read value from digital port.'),
    _('Set HIGH value for digital port.'),
    _('Configure Arduino port for digital input.'),
    _('Configure Arduino port to drive a servo.'),
    _('Set LOW value for digital port.'),
    _('Configure Arduino port for digital output.'),
    _('Configure Arduino port for PWM (pulse-width modulation).')
]

EXPEYES_STRINGS = [
    #TRANS: plugin to control an ExpEyes device
    _("Palette of Expeyes blocks"),
    # TRANS: Programmable voltage output
    _("set PVS"),
    _("set programmable voltage output"),
    # TRANS: Square wave 1 voltage output
    _("set SQR1 voltage"),
    _("set square wave 1 voltage output"),
    # TRANS: Square wave 2 voltage output
    _("set SQR2 voltage"),
    _("set square wave 2 voltage output"),
    # TRANS: Digital output level
    _("set OD1"),
    _("set digital output level (OD1) low (0) or high (1)"),
    # TRANS: Input 1 voltage level
    _("IN1 level"),
    _("returns 1 if IN1 voltage level >2.5 volts, 0 if IN1 voltage level \
<= 2.5 volts"),
    # TRANS: Input 2 voltage level
    _("IN2 level"),
    _("returns 1 if IN2 voltage level >2.5 volts, 0 if IN2 voltage level \
<= 2.5 volts"),
    # TRANS: Resistive sensor voltage level
    _("SEN level"),
    _("returns 1 if resistive sensor (SEN) voltage level > 2.5 volts, 0 if SEN \
voltage level <= 2.5 volts"),
    _("capture"),
    _("input"),
    _("samples"),
    _("interval"),
    # TRANS: MS is microseconds
    _("capture multiple samples from input at interval (MS); results pushed \
to FIFO"),
    # TRANS: Analog input 1 voltage level
    _("A1"),
    _("read analog input 1 voltage"),
    # TRANS: Analog input 2 voltage level
    _("A2"),
    _("read analog input 2 voltage"),
    # TRANS: Read input 1 voltage
    _("IN1"),
    _("read input 1 voltage"),
    # TRANS: Read input 2 voltage
    _("IN2"),
    _("read input 2 voltage"),
    # TRANS: Read analog sensor input voltage
    _("SEN"),
    _("read analog sensor input voltage"),
    # TRANS: Read square wave 1 input voltage
    _("SQR1"),
    _("read square wave 1 voltage"),
    # TRANS: Read square wave 2 input voltage
    _("SQR2"),
    _("read square wave 2 voltage"),
    # TRANS: Read programmable voltage
    _("PVS"),
    _("read programmable voltage"),
    _("Expeyes device not found")
]
