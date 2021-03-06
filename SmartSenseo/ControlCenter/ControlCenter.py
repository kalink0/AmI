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

#from XMLFileManager import XMLFileManager
from SerialConnection import SerialConnection
import struct

class ControlCenter (object) :
    def __init__(self) :
        self.__status = 0   # 2^0 = on/off, 2^1 = water, 2^2 = job, 2^3 = cup 
        self.rfid = 0
        self.__nameofchip = ''
        self.__numbersofchip = -1

        self.__serialconnection = SerialConnection.SerialConnection()
        #self.__filemanager = XMLFileManager.XMLFileManager()
        self.__cupchanged = 0

    def __del__(self) :
        #self.__filemanager.writeToFile (self.__rfid, self.__nameofchip, self.__numbersofchip)
        #self.__filemanager.__del__
        self.__serialconnection.__del__


    '''method to get the status of the machine (on or off)'''
    def getStatus (self) :
        statusbyte = self.__serialconnection.getStatusByte()
        self.__status = struct.unpack("B", statusbyte[0])[0]  & 0x0F
        return self.__status

    def fillCup (self, size) :
        #if ((self.__status & 0xff) == 0x0B) :
        if size == 1 :
            self.__serialconnection.sendControlByte(0x0A)   #0000 1010
        else :
            self.__serialconnection.sendControlByte(0x0C)   #0000 1100
        self.__numbersofchip += 1
        while 1 :   # waiting for finishing the job
            if (self.getStatus() & 0x04) == 0 :
                break
        print "Job finished, enjoy your coffee!"

    '''get RFIDNumber of the cup in the Machine'''
    def getRFIDNumberFromMachine (self) :
        self.__cupchanged = 0
        temp_rfid = self.__serialconnection.getRFID()
        if temp_rfid != self.__rfid and self.__rfid != 0:   #if cup has changed, write the old data into the xml file
            self.__filemanager.writeToFile(self.__rfid, self.__nameofchip, self.__numberofchip);
            self.__cupchanged = 1
        self.__rfid = temp_rfid
        return self.__rfid

    def searchUsedRFID (self) :
        chipData = self.__filemanager.readFromFile(self.__rfid)
        if chipData.chipid != -1 :
            self.__nameofchip = chipData.name
            self.__numbersofchip = chipData.numbers
        else :
            self.__nameofchip = input ("The cup is unknown, please enter a name for it: ")    
            
    def assignNameToRFID (self, name) :
        self.__nameofchip = name

    def switchStatus (self) :
        self.__serialconnection.sendControlByte(0x09)