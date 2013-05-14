# -*- coding: utf-8 -*-
#SmartSenseo Serial Connection
#Copyright (C) 2013  Marco Neumann, Nils Buerkner

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import serial
import array

class SerialConnection(object):

    def __init__(self):
        self.__portin = serial.Serial('COM6', 9600, timeout = 5)
        #self.__portout = serial.Serial('COM2', 9600)
        self.__statusbyte = array.array('B', [0xff,0xff,0xff,0xff,0xff])

    def __del__(self) :
        #self.__portout.close()
        self.__portin.close()
        
    def sendControlByte (self, control) :
        self.__portin.write(control)
        self.__statusbyte = self.__portin.read(5)
        
    def getRFID (self) :
        self.getStatusByte()
        temp = [self.__statusbyte[1], self.__statusbyte[2], self.__statusbyte[3], self.__statusbyte[4]]
        return int(''.join(map(str,temp)))
        
    def getStatusByte (self) :
        self.sendControlByte(0x08)
        return self.__statusbyte