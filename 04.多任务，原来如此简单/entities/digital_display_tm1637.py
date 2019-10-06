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
import re
from .ic_tm1637 import IC_TM1637 as IC_TM1637

class DigitalDisplayTM1637(object):
    '''
    Digital display class
    '''

    __ic_tm1637 = None
    __numbers = []
    __number_code = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x00, 0x40]
    __address_code = [0xc0, 0xc1, 0xc2, 0xc3]
    __is_on = False


    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the digital display
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__ic_tm1637 = IC_TM1637(pins, real_true)

    #Stauts.
    @property
    def is_on(self):
        '''
        Get the current status of the digital display
        '''
        return self.__is_on

    @property
    def numbers(self):
        '''
        Get the current numbers array showing
        :return: numbers array
        '''
        return self.__numbers

    #@numbers.setter
    def set_numbers(self, value):
        '''
        Set the numbers array to show
        :return: void
        '''
        pattern = re.compile(r'[-|#|\d]\.?')
        matches = pattern.findall(value)
        #del self.__numbers
        self.__numbers = []
        for i in range(len(matches)):
            self.__numbers.append(matches[i])
        #print(self.__numbers)

    #@numbers.deleter
    #def numbers(self):
    #    del self.__numbers

    @property
    def ic(self):
        '''
        Return the instance of ic
        :return: ic
        '''
        return  self.__ic_tm1637

    #Verbs.
    def on(self):
        '''
        Set display on
        :return: void
        '''
        self.__ic_tm1637.set_command(0x8f)
        self.__is_on = True

    def off(self):
        '''
        Set display off
        :return: void
        '''
        self.__ic_tm1637.clear()
        self.__is_on = False

    def show(self, str):
        '''
        Set the numbers array to show and enable the display
        :return: void
        '''
        self.set_numbers(str)
        #print(self.__numbers)

        self.__ic_tm1637.set_command(0x44)

        for i in range(min(4, len(self.__numbers))):
            dp = True if self.__numbers[i].count('.') > 0 else False
            num = self.__numbers[i].replace('.','')
            if num == '#':
                num = 10
            elif num == '-':
                num = 11
            else:
                num = int(num)

            if dp:
                self.__ic_tm1637.set_data(self.__address_code[i], self.__number_code[num]|0x80)
            else:
                self.__ic_tm1637.set_data(self.__address_code[i], self.__number_code[num])

        self.on()
