#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 NXEZ.COM.
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
from .ic_74hc595 import IC_74HC595 as IC_74HC595

class Led74HC595(object):
    '''
    Class of leds in 74HC595
    '''
    __ic_74hc595 = None

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the leds
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__ic_74hc595 = IC_74HC595(pins, real_true)

    #Stauts.
    @property
    def ic(self):
        return  self.__ic_74hc595

    def is_on(self, index):
        '''
        Get status of led in ledrow by index
        :param index: index of the led
        :return: status in boolean
        '''
        if index >= 8:
            return False
        return self.__ic_74hc595.data >> index & 0x01

    @property
    def row_status(self):
        '''
        Get status array of the ledrow
        :return: status array
        '''
        r = []
        for i in range (0, 8):
            r.append(self.__ic_74hc595.data >> i & 0x01)
        return r

    #Verbs.
    def on(self):
        '''
        Set all the leds on
        :return: void
        '''
        self.__ic_74hc595.set_data(0xff)

    def off(self):
        '''
        Set all the leds off
        :return: void
        '''
        self.__ic_74hc595.clear()

    def on_for_index(self, index):
        '''
        Set the led on by index in the ledrow
        :return: void
        '''
        self.__ic_74hc595.set_data(self.__ic_74hc595.data | (0x01 << (index)))

    def off_for_index(self, index):
        '''
        Set the led off by index in the ledrow
        :return: void
        '''
        arr = [0xfe, 0xfd, 0xfb, 0xf7, 0xef, 0xdf, 0xbf, 0x7f]
        self.__ic_74hc595.set_data(self.__ic_74hc595.data & arr[index])

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
                self.on_for_index(i)
            else:
                self.off_for_index(i)
