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
import array

class BluetoothConnection(object):
    
    def __init__(self, mac_address="00:02:72:b1:9e:e0"):
        try:
            self.__socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.__socket.connect((mac_address, 30))
        except socket.error:
            self.__socket.close()
            raise SystemExit('Error, problem with socket!')
        self.__controlbyte = 0x00
        self.__statusbyte = array.array('B', [0xff,0xff,0xff,0xff,0xff])

        
    def __del__(self) :
        self.__socket.close()
        
    def sendControlByte (self, control) :
        print(self.__statusbyte[0])
        self.__socket.send(str(control).encode(encoding='utf_8'))
        self.__socket.recv_into(self.__statusbyte)
        print(self.__statusbyte[0])
        
    def getRFID (self) :
        self.getStatusByte()
        if not self.__statusbyte[4] ==  (self.__rfid >> 24 ) :  #Vergleich ob neue Tasse drunter steht
            temp = [self.__statusbyte[1], self.__statusbyte[2], self.__statusbyte[3], self.__statusbyte[4]]
        return int(''.join(map(str,temp)))
        
    def getStatusByte (self) :
        self.sendControlByte("8".encode(encoding='utf_8', errors='strict'))
        return self.__statusbyte