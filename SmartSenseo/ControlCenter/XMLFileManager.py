#XMLFileManager.py, Project in Ambient Intelligence, Read and Write XMLFiles
#Copyright (C) 2013  Marco Neumann, Nils Bürkner

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

class XMLFileManager(object):
    def __init__ (self) :
        self.__filename = "cups.xml" #fix name in this project, there is no need for a changeable filename

    def writeToFile (self) :
        doc = ElementTree(file = self.__filename);
        

    def readFromFile (self) :
        doc = ElementTree(file = self.__filename);


