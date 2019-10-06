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

class SAKSPins(object):
    '''
    SAKS Pins Code With BCM for Raspberry Pi.
    '''

    IC_74HC595_DS = 6
    IC_74HC595_SHCP = 19
    IC_74HC595_STCP = 13

    IC_TM1637_DI = 25
    IC_TM1637_CLK = 5

    BUZZER = 12

    TACT_RIGHT = 20
    TACT_LEFT = 16
    DIP_SWITCH_1 = 21
    DIP_SWITCH_2 = 26

    IR_SENDER = 17
    IR_RECEIVER = 9
    DS18B20 = 4
    UART_TXD = 14
    UART_RXD = 15
    I2C_SDA = 2
    I2C_SLC = 3