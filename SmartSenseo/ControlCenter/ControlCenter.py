#SmartSenseo Control Center, Project in Ambient Intelligence, Controlling a Senseo Machine via Bluetooth
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

from XMLFileManager import XMLFileManager
from BluetoothConnection import BluetoothConnection

class ControlCenter (object) :
    def __init__(self) :
        self.__status = 0
        self.__rfid = 0
        self.__nameofchip = '';
        self.__numbersofchip = -1;
        self.__btconnection = BluetoothConnection()
        self.__filemanager = XMLFileManager()

    def __del__(self) :
        self.__filemanager.writeToFile (self.__rfid, self.__nameofchip, self.__numberofchip)
        self.__filemanager.__del__
        self.__bconnection.__del__

    def getStatus (self) :
        statusbyte = self.__btconnection.getStatusByte()
        return self.__status

    def fillCup (self, size) :
        if size == 1 :
            self.__btconnection.sendControlByte(0x0A)   #0000 1010
        else :
            self.__btconnection.sendControlByte(0x0C)   #0000 1100
        #TODO Receiving and controlling of the bytes
        #TODO Exceptionhandling?
        #TODO return?

    def getRFIDNumberFromMachine (self) :
        self.__rfid = self.__btconnection.getRFID()
        return self__rfid

    def searchUsedRFID (self) :
        self.__filemanager.readFromFile(self.__rfid)

    def assignNameToRFID (self, name) :
        self.nameofchip = name

    def switchStatus (self) :
        self.__btconnection.sendControlByte(0x09)
        #TODO: Confirmation