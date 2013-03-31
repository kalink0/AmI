#BluetoothConnection.py, Project in Ambient Intelligence, Realization of the connection to
#SmartSenseo Machine
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

import socket

class BluetoothConnection(object):
    
    def __init__(self, mac_address="F0:7B:CB:F2:5F:1C"):
        self.__socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.__socket.connect((mac_address, 1))
        self.__controlbyte = 0x00
        self.__statusbyte =  [-1,-1,-1,-1,-1]
        
    def __del__(self) :
        self.__socket.close()
        
    def sendControlByte (self, control) :
        self.__socket.send(control)
        self.__socket.recv_into(self.__statusbyte, 5)
        
        
    def getRFID (self) :
        self.getStatusByte()
        if not self.__statusbyte[4] ==  (self.__rfid >> 24 ) :  #Vergleich ob neue Tasse drunter steht
            temp = [self.__statusbyte[1], self.__statusbyte[2], self.__statusbyte[3], self.__statusbyte[4]]
        return int(''.join(map(str,temp)))
        
    def getStatusByte (self) :
        self.sendControlByte(0x08)
        return self.__statusbyte