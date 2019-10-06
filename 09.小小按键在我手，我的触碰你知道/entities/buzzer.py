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

class Buzzer(object):
    '''
    Buzzer class
    '''
    __pin = 0
    __real_true = GPIO.HIGH
    __is_on = False

    def __init__(self, pin, real_true = GPIO.HIGH):
        '''
        Init the buzzer
        :param pin: pin number
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pin = pin
        self.__real_true = real_true

    #Stauts.
    @property
    def is_on(self):
        '''
        Return the status of buzzer
        :return: void
        '''
        return self.__is_on

    #Verbs.
    def on(self):
        '''
        Set buzzer on
        :return: void
        '''
        GPIO.output(self.__pin, self.__real_true)
        self.__is_on = True

    def off(self):
        '''
        Set buzzer off
        :return: void
        '''
        GPIO.output(self.__pin, not self.__real_true)
        self.__is_on = False

    #functions.
    def beep(self, seconds):
        '''
        Beep one time
        :param seconds: beep time
        :return: void
        '''
        self.on()
        time.sleep(seconds)
        self.off()

    def beepAction(self, secs, sleepsecs, times):
        '''
        Beep in a rhythm
        e.g. beepAction(0.02,0.02,30)
        :param secs: beep time
        :param sleepsecs: break time
        :param times: repeat times
        :return: void
        '''
        for i in range(times):
            self.beep(secs)
            time.sleep(sleepsecs)
