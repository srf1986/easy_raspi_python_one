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

class IC_74HC595(object):
    '''
    IC_74HC595 class
    '''
    __pins = {'ds':0, 'shcp':0, 'stcp':0}
    __real_true = GPIO.HIGH
    __data = 0x00

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the ic
        :param pin: pin number
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pins = pins
        self.__real_true = real_true

    #Stauts.
    @property
    def data(self):
        '''
        Return the data
        :return: void
        '''
        return self.__data

    #Verbs.
    def flush_shcp(self):
        '''
        Flush a shcp
        :return: void
        '''
        GPIO.output(self.__pins['shcp'], not self.__real_true)
        GPIO.output(self.__pins['shcp'], self.__real_true)

    def flush_stcp(self):
        '''
        Flush a stcp
        :return: void
        '''
        GPIO.output(self.__pins['stcp'], not self.__real_true)
        GPIO.output(self.__pins['stcp'], self.__real_true)

    def set_bit(self, bit):
        '''
        Set a bit
        :param bit: bit
        :return: void
        '''
        GPIO.output(self.__pins['ds'], bit)
        self.flush_shcp()

    def set_data(self, data):
        '''
        Set a byte
        :param data: data
        :return: void
        '''
        self.__data = data
        for i in range (0, 8):
            self.set_bit((self.__data >> i) & 0x01)

        self.flush_stcp()


    def clear(self):
        '''
        Clear the data
        :return: void
        '''
        self.set_data(0x00)
