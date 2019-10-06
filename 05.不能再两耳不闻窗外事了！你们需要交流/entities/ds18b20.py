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

import time
import subprocess
import os
import glob

class DS18B20(object):
    '''
    DS18B20 class
    '''
    __pin = 0 #it's no use
    #__device_file = ''
    #__temperature = -128

    def __init__(self, pin = 4):
        '''
        Init the DS18b20
        :param pin: pin number
        :return: void
        '''
        self.__pins = pin
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-therm')

    #Verbs.
    def get_device_file(self, index = 0):
        base_dir = '/sys/bus/w1/devices/'
        #fix "IndexError: list index out of range"
        if not glob.glob(base_dir + '28*'):
            return False
        if glob.glob(base_dir + '28*')[index] is not None:
            device_folder = glob.glob(base_dir + '28*')[index]
            return device_folder + '/w1_slave'
        else:
            return False

    def read_temp_raw(self, index = 0):
        df = self.get_device_file(index)
        if not df:
            return False
        catdata = subprocess.Popen(['cat', df], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

    def read_temp(self, index = 0):
        tr = self.read_temp_raw(index)
        if not tr:
            return False
        lines = tr
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            tr = self.read_temp_raw(index)
            if not tr:
                return False
            lines = tr
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            #return temp_c, temp_f
            return temp_c

    #Stauts.
    @property
    def is_exist(self, index = 0):
        '''
        Return true if the ds18b20 is exist
        :param index: from 0 to n
        :return: Return true if the ds18b20 is exist
        '''
        #if not os.path.exists(self.__device_file):
        #    return False
        #else:
        #    return True
        return self.get_device_file(index)

    @property
    def temperature(self, index = 0):
        '''
        Get the temperature from ds18b20
        :param index: from 0 to n
        :return: Return the temperature from ds18b20, return -128 means get a error.
        '''
        if not self.is_exist:
            return -128.0
        else:
            return self.read_temp(index)
