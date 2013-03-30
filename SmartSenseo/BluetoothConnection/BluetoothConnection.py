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
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.socket.connect((mac_address, 1))
        