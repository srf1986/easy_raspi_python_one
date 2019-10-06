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

class Tact(object):
    '''
    Tact class
    '''
    __pin = 0
    __real_true = GPIO.HIGH
    __status = False

    __observers = []

    def __init__(self, pin, real_true = GPIO.HIGH):
        '''
        Init the tact
        :param pin: pin number in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pin = pin
        self.__real_true = real_true

        if self.__real_true:
            self.__status = GPIO.input(self.__pin)
        else:
            self.__status = not GPIO.input(self.__pin)

        GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.make_event, bouncetime = 1)

        try:
            t1 = Thread(target = self.watching)
            t1.setDaemon(True)
            #t1.start()
        except:
            print("Error: Unable to start thread by Tact")


    #Stauts.
    @property
    def is_on(self):
        '''
        Get current of tact
        '''
        if self.__real_true:
            if self.__status != GPIO.input(self.__pin):
                self.__status = GPIO.input(self.__pin)
        else:
            if self.__status == GPIO.input(self.__pin):
                self.__status = not GPIO.input(self.__pin)

        return self.__status

    #Events
    def register(self, observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def deregister(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self, status):
        for o in self.__observers:
            o.on_tact_event(self.__pin, status)

    def event(self, action):
        self.notify_observers(action)

    def make_event(self, channel):
        self.notify_observers(self.__real_true if GPIO.input(self.__pin) else not self.__real_true)
        if self.__real_true:
            if self.__status != GPIO.input(self.__pin):
                self.__status = GPIO.input(self.__pin)
                #self.notify_observers(self.__real_true if self.__status else not self.__real_true)
        else:
            if self.__status == GPIO.input(self.__pin):
                self.__status = not GPIO.input(self.__pin)
                #self.notify_observers(self.__real_true if not self.__status else not self.__real_true)

    def watching(self):
        if self.__real_true:
            while True:
                if GPIO.input(self.__pin) != self.__status:
                    self.__status = GPIO.input(self.__pin)
                    self.notify_observers(self.__real_true if self.__status else not self.__real_true)
                    time.sleep(0.05)
        else:
            while True:
                if GPIO.input(self.__pin) == self.__status:
                    self.__status = not GPIO.input(self.__pin)
                    self.notify_observers(self.__real_true if not self.__status else not self.__real_true)
                    time.sleep(0.05)

class TactRow(object):
    '''
    Class of tacts in row
    '''
    __tacts = []
    __pins = []
    __real_true = GPIO.HIGH

    def __init__(self, pins, real_true = GPIO.HIGH):
        '''
        Init the tacts
        :param pin: pin numbers in array
        :param real_true: GPIO.HIGH or GPIO.LOW
        :return: void
        '''
        self.__pins = pins
        self.__real_true = real_true
        for p in pins:
            self.__tacts.append(Tact(p, real_true))

    #Stauts.
    def is_on(self, index):
        '''
        Get status of tact in tactrow by index
        :param index: index of the tact
        :return: status in boolean
        '''
        if index >= len(self.__tacts):
            return False
        return self.__tacts[index].is_on

    @property
    def row_status(self):
        '''
        Get status array of the tactrow
        :return: status array
        '''
        r = []
        for l in self.__tacts:
            r.append(l.is_on)
        return r

    @property
    def items(self):
        '''
        Get the instances of the tacts in tactrow
        :return: instances array
        '''
        return self.__tacts
