#XMLFileManager.py, Project in Ambient Intelligence, Read and Write XMLFiles
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

from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as xmltree

class XMLFileManager(object):
    def __init__ (self) :
        self.__filename = "cups.xml" #fix name in this project, there is no need for a changeable filename

    """Method to overwrite the values of existing chips or append a new chip with values"""
    def writeToFile (self, rfid, nameofchip, numberofchip) :
        doc = ElementTree(file = self.__filename);
        root = doc.getroot()
        for chips in root.getchildren():
            chipid = int((chips.find('chip-id')).text)
            if chipid == rfid :  #if id is already in the xml, delete the tuple
                root.remove(chips)
        #create the new Element for the ElementTree
        chip = xmltree.Element('chips')
        chip_id = xmltree.Element('chip-id')
        chip_id.text = ElementTree.__str__(rfid)
        name = xmltree.Element('name')
        name.text = nameofchip
        numbers = xmltree.Element('numbers')
        numbers.text = ElementTree.__str__(numberofchip)
        chip.insert(0, chip_id)
        chip.insert(1, name)
        chip.insert(2, numbers)
        # and append it to the existing tree
        root.append(chip)
        xmltree.ElementTree(root).write(self.__filename)        

    """Method to search for the chip number, if chip number cannot be found, the returned id will be -1"""
    def readFromFile (self, rfid) :
        doc = ElementTree(file = self.__filename);
        root = doc.getroot()
        for chips in root.getchildren():
            chipid = int((chips.find("chip-id")).text)
            name = (chips.find("name")).text
            numbers = int((chips.find("numbers")).text)
            if chipid == rfid :
                chip_data = (chipid, name, numbers) #store the data in one tuple for return
                return chip_data
            chip_data = (-1, "", -1) # if id isn't found
        return chip_data

