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

# PLUGINS

CURRENCY_STRINGS = [
    _('Palette of Mexican pesos'),
    _('Palette of Colombian pesos'),
    _('Palette of Rwandan francs'),
    _('Palette of US currencies'),
    _('Palette of Australian currencies'),
    _('Palette of Guaranies')
    ]

BUTIA_STRINGS = [
    #TRANS: Butia is the Arduino Robot Project from Uruguay
    #(http://www.fing.edu.uy/inco/proyectos/butia/)
    _('Turtle Art Butia'),
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
    _('LED'),
    _('pushbutton'),
    _('grayscale'),
    _('ambient light'),
    _('temperature'),
    _('distance'),
    _('tilt'),
    _('magnetic induction'),
    _('vibration'),
    _('Butia Robot'),
    _('delay Butia'),
    _('wait for argument seconds'),
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
    #TRANS: This string is shorthand for "move Butia backward"
    _('backward Butia'),
    _('move the Butia robot backward'),
    _('move the Butia robot backward a predefined distance'),
    #TRANS: This string is shorthand for "turn Butia left"
    _('left Butia'),
    _('turn the Butia robot at left'),
    #TRANS: This string is shorthand for "turn Butia right"
    _('right Butia'),
    _('turn the Butia robot at right'),
    _('turn Butia'),
    _('turn the Butia robot x degrees'),
    _('stop Butia'),
    _('stop the Butia robot'),
    _('display Butia'),
    #TRANS: this string must contain only ASCII characters.
    #The len must be 32 characters/spaces.
    _('Hello World    Butia            '),
    _('print text in Butia robot 32-character ASCII display'),
    _('Butia')
    ]

FOLLOWME_STRINGS = [
    _('The camera was not found.'),
    _('Error on the initialization of the camera.'),
    _('FollowMe'),
    _('follow a RGB color'),
    _('set a threshold for a RGB color'),
    _('follow a turtle color'),
    _('set the minimal number of pixels to follow'),
    _('calibrate'),
    _('calibrate a color to follow'),
    _('x position'),
    _('return x position'),
    _('y position'),
    _('return y position'),
    _('pixels'),
    _('return the number of pixels of the biggest blob')
    ]

SUMO_STRINGS = [
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
    _('angle to center'),
    #TRANS: dohyo is the playing field
    _('get the angle to the center of the dohyo'),
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
    _('Save the project to the Journal as a Physics activity.'),
    _('density'),
    _('Set the density property for objects \
(density can be any positive number).'),
    _('friction'),
    _('Set the friction property for objects (value from 0 to 1, \
where 0 turns friction off and 1 is strong friction).'),
    # TRANS: bounciness is restitution
    _('bounciness'),
    _('Set the bounciness property for \
objects (a value from 0 to 1, where 0 means no bounce and 1 is very bouncy).'),
    _('dynamic'),
    _('If dynamic = 1, the object can move; \
if dynamic = 0, it is fixed in position.')
]

WEDO_STRINGS = [
    # TRANS: WeDo is a robotics product of the LEGO company
    _('Palette of WeDo blocks'),
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
    _('set the value for Motor B')
]

LEGO_STRINGS = [
    # TRANS: Lego NXT is a robotics product of the LEGO company
    _('Palette of LEGO NXT blocks'),
    _('touch'),
    _('ultrasonic'),
    _('color'),
    _('light'),
    _('PORT A'),
    _('PORT B'),
    _('PORT C'),
    _('PORT 1'),
    _('PORT 2'),
    _('PORT 3'),
    _('PORT 4'),
    _('Please check the connection with the brick.'),
    _('Please check the port.'),
    _('The value of power must be between -127 to 127.'),
    _('An error has ocurred: check all and try reconnect.'),
    _('NXT found'),
    _('NXT not found'),
    _('refresh NXT'),
    _('Search for a connected NXT brick.'),
    _('play tone'),
    _('freq'),
    _('time'),
    _('Play a tone at freq for time.'),
    _('turn motor\nrotations'),
    _('port'),
    _('power'),
    _('turn a motor'),
    _('sync motors\nsteering'),
    _('rotations'),
    _('synchronize two motors'),
    _('PORT A of the brick'),
    _('PORT B of the brick'),
    _('PORT C of the brick'),
    _('start motor'),
    _('Run a motor forever.'),
    _('brake motor'),
    _('Stop a specified motor.'),
    _('PORT 1 of the brick'),
    _('color sensor'),
    _('light sensor'),
    _('PORT 2 of the brick'),
    _('touch sensor'),
    _('distance sensor'),
    _('PORT 3 of the brick'),
    _('read'),
    _('sensor'),
    _('Read sensor output.'),
    _('PORT 4 of the brick'),
    _('set light'),
    _('Set color sensor light.'),
    _('reset motor'),
    _('Reset the motor counter.'),
    _('motor position'),
    _('Get the motor position.')
]

ARDUINO_STRINGS = [
    #TRANS: Arduino plugin to control an Arduino board
    _('Palette of Arduino blocks'),
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

