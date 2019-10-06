#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 NXEZ.COM.
# http://www.nxez.com
#
# Licensed under the GNU General Public License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.gnu.org/licenses/gpl-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import RPi.GPIO as GPIO
import time
from threading import Thread

class Led(object):
    '''
    Led class
    '''
    __pin = 0
    __real_true = GPIO.HIGH
    __pwm = None
    __is_on = False
    __is_pulse = None

    def __init__(self, pin, real_true = GPIO.HIGH):
        '''
        Init the led
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pin = pin
        self.__real_true = real_true

    #Stauts.
    @property
    def is_on(self):
        '''
        Get the current status of the led
        '''
        return self.__is_on

    #Verbs.
    def on(self):
        '''
        Set the led on
        '''
        if not self.__is_pulse:
            GPIO.output(self.__pin, self.__real_true)
            self.__is_on = True

    def off(self):
        '''
        Set the led off
        '''
        if self.__is_pulse:
            self.__is_pulse = False
            self.__pwm.stop()
            time.sleep(0.1)
        GPIO.output(self.__pin, not self.__real_true)
        self.__is_on = False

    #functions.
    def flash(self, seconds):
        '''
        Flash one time
        :param seconds: on time
        :return: void
        '''
        self.on()
        time.sleep(seconds)
        self.off()

    #e.g. flashAction(0.02,0.02,30)
    def flashAction(self, secs, sleepsecs, times):
        '''
        Flash in a rhythm
        e.g. flashAction(0.02,0.02,30)
        :param secs: on time
        :param sleepsecs: break time
        :param times: repeat times
        :return: void
        '''
        for i in range(times):
            self.flash(secs)
            time.sleep(sleepsecs)

    def pulse(self, hertz=50, pause_time=0.01):
        '''
        Breath until led off
        :param hertz: GPIO PWM hertz
        :param pause_time: breath pause time
        :return: void
        '''
        if self.__pwm == None:
            self.__pwm = GPIO.PWM(self.__pin, hertz)
        else:
            self.__pwm.ChangeFrequency(hertz)
        self.__pwm.start(0)
        if self.__is_pulse == None:
            def pulse_worker():
                while True:
                    if self.__is_pulse:
                        try:
                            for i in xrange(0, 101, 1):
                                self.__pwm.ChangeDutyCycle(i)
                                # off
                                time.sleep(pause_time)
                            time.sleep(1)
                            for i in xrange(100, -1, -1):
                                self.__pwm.ChangeDutyCycle(i)
                                # on
                                time.sleep(pause_time)
                        except:
                            continue
            try:
                pulse_thread = Thread(target = pulse_worker)
                pulse_thread.setDaemon(True)
                pulse_thread.start()
            except:
                print('Error: Unable to start thread by Led')
        self.__is_pulse = True
        self.__is_on = True

class LedRow(object):
    '''
    Class of leds in row
    '''
    __leds = []
    __pins = []
    __real_true = GPIO.HIGH

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the leds
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pins = pins
        self.__real_true = real_true
        for p in pins:
            self.__leds.append(Led(p, real_true))

    #Stauts.
    #@property
    def is_on(self, index):
        '''
        Get status of led in ledrow by index
        :param index: index of the led
        :return: status in boolean
        '''
        if index >= len(self.__leds):
            return False
        return self.__leds[index].is_on

    @property
    def row_status(self):
        '''
        Get status array of the ledrow
        :return: status array
        '''
        r = []
        for l in self.__leds:
            r.append(l.is_on)
        return r

    @property
    def items(self):
        '''
        Get the instances of the leds in ledrow
        :return: instances array
        '''
        return self.__leds

    #Verbs.
    #@multimethod()
    def on(self):
        '''
        Set all the leds on
        :return: void
        '''
        for l in self.__leds:
            l.on()

    #@multimethod()
    def off(self):
        '''
        Set all the leds off
        :return: void
        '''
        for l in self.__leds:
            l.off()

    #@multimethod(int)
    def on_for_index(self, index):
        '''
        Set the led on by index in the ledrow
        :return: void
        '''
        self.__leds[index].on()

    #@multimethod(int)
    def off_for_index(self, index):
        '''
        Set the led off by index in the ledrow
        :return: void
        '''
        self.__leds[index].off()

    def set_row(self, status):
        '''
        Set the ledrow's status in boolean array
        :param status: boolean array
        :return: void
        '''
        for i in range(len(status)):
            #print(str(i) + str(status[i]))
            if status[i] is None:
                continue
            if status[i]:
                self.__leds[i].on()
            else:
                self.__leds[i].off()
