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

class ControlCenter (object) :
    def __init__(self) :
        self.__status = 0
        self.__rfid = 0
        self.__nameofchip = '';
        self.__numbersofchip = -1;
        #self.__btconnection = BluetoothConnection()
        self.__filemanager = XMLFileManager()

    def __del__(self) :
        #TODO Write into file
        #TODO Close Bluetooth connection

    def getStatus (self) :
        #TODO Call getStatusByte from btconnection
        return self.__status

    def fillCup (self, size) :
        #TODO call sendControlBYte and call getStatusBYte
        #TODO Exceptionhandling?
        #TODO return?

    def getRFIDNumberFromMachine (self) :
        #TODO call getRFID

    def searchUsedRFID (self) :
        #TODO Read from File

    def assignNameToRFID (self, name) :
        self.nameofchip = name

    def switchStatus (self) :
        #TODO call sendControlByte