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

class DipSwitch2Bit(object):
    '''
    Dip switch (2bit) class
    '''
    __pins = []
    __real_true = GPIO.HIGH
    __status = []

    __observers = []

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the dip switch
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pins = pins
        self.__real_true = real_true
        for p in pins:
            self.__status.append(not real_true)

        if self.__real_true:
            self.__status[0] = GPIO.input(self.__pins[0])
            self.__status[1] = GPIO.input(self.__pins[1])
        else:
            self.__status[0] = not GPIO.input(self.__pins[0])
            self.__status[1] = not GPIO.input(self.__pins[1])


        GPIO.add_event_detect(self.__pins[0], GPIO.BOTH, callback = self.make_event, bouncetime = 50)
        GPIO.add_event_detect(self.__pins[1], GPIO.BOTH, callback = self.make_event, bouncetime = 50)

        try:
            t1 = Thread(target = self.watching)
            t1.setDaemon(True)
            #t1.start()
        except:
            print("Error: Unable to start thread by DipSwitch")

    #Stauts.
    @property
    def is_on(self):
        '''
        Get the status of each bit
        :return: the status array
        '''
        return self.__status

    #Events
    def register(self, observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def deregister(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self):
        for o in self.__observers:
            #o.update(self.__status)
            o.on_dip_switch_2bit_status_changed(self.__status)

    def status_changed(self):
        self.notify_observers()

    def make_event(self, channel):
        if self.__real_true:
            if GPIO.input(self.__pins[0]) != self.__status[0]:
                self.__status[0] = GPIO.input(self.__pins[0])
                self.status_changed()

            if GPIO.input(self.__pins[1]) != self.__status[1]:
                self.__status[1] = GPIO.input(self.__pins[1])
                self.status_changed()
        else:
            if GPIO.input(self.__pins[0]) == self.__status[0]:
                self.__status[0] = not GPIO.input(self.__pins[0])
                self.status_changed()

            if GPIO.input(self.__pins[1]) == self.__status[1]:
                self.__status[1] = not GPIO.input(self.__pins[1])
                self.status_changed()

    def watching(self):
        if self.__real_true:
            while True:
                if GPIO.input(self.__pins[0]) != self.__status[0]:
                    self.__status[0] = GPIO.input(self.__pins[0])
                    self.status_changed()

                if GPIO.input(self.__pins[1]) != self.__status[1]:
                    self.__status[1] = GPIO.input(self.__pins[1])
                    self.status_changed()

                time.sleep(0.05)
        else:
            while True:
                if GPIO.input(self.__pins[0]) == self.__status[0]:
                    self.__status[0] = not GPIO.input(self.__pins[0])
                    self.status_changed()

                if GPIO.input(self.__pins[1]) == self.__status[1]:
                    self.__status[1] = not GPIO.input(self.__pins[1])
                    self.status_changed()

                time.sleep(0.05)
