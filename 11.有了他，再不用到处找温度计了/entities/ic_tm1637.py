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
import time

class IC_TM1637(object):
    '''
    IC_TM1637 class
    '''
    __pins = {'di' : 0, 'clk' : 0}
    __real_true = GPIO.HIGH

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the ic
        :param pin: pin number
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pins = pins
        self.__real_true = real_true

    #Verbs.
    def bus_delay(self):
        '''
        Delay
        :return: void
        '''
        time.sleep(0.001)

    def start_bus(self):
        '''
        Start bus
        :return: void
        '''
        GPIO.output(self.__pins['clk'], self.__real_true)
        GPIO.output(self.__pins['di'], self.__real_true)
        self.bus_delay()
        GPIO.output(self.__pins['di'], not self.__real_true)
        self.bus_delay()
        GPIO.output(self.__pins['clk'], not self.__real_true)
        self.bus_delay()

    def stop_bus(self):
        '''
        Stop bus
        :return: void
        '''
        GPIO.output(self.__pins['clk'], not self.__real_true)
        self.bus_delay()
        GPIO.output(self.__pins['di'], not self.__real_true)
        self.bus_delay()
        GPIO.output(self.__pins['clk'], self.__real_true)
        self.bus_delay()
        GPIO.output(self.__pins['di'], self.__real_true)
        self.bus_delay()

    def set_bit(self, bit):
        '''
        Set a bit
        :param bit: bit
        :return: void
        '''
        GPIO.output(self.__pins['clk'], not self.__real_true)
        self.bus_delay()
        GPIO.output(self.__pins['di'], bit)
        self.bus_delay()
        GPIO.output(self.__pins['clk'], self.__real_true)
        self.bus_delay()

    def set_byte(self, data):
        '''
        Set a byte
        :param data: data
        :return: void
        '''
        for i in range (0, 8):
            self.set_bit((data >> i) & 0x01)

        GPIO.output(self.__pins['clk'], not self.__real_true)
        self.bus_delay()

        GPIO.output(self.__pins['di'], self.__real_true)
        self.bus_delay()

        GPIO.output(self.__pins['clk'], self.__real_true)
        self.bus_delay()

    def set_command(self, command):
        '''
        Set command
        :param command: command code
        :return: void
        '''
        self.start_bus()
        self.set_byte(command)
        self.start_bus()

    def set_data(self, address, data):
        '''
        Set data with address and data
        :param address: address
        :param data: data
        :return: void
        '''
        self.start_bus()
        self.set_byte(address)
        self.set_byte(data)
        self.start_bus()

    def clear(self):
        '''
        Clear the data
        :return: void
        '''
        self.set_command(0x80)
