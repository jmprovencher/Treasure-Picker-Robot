from TCPServer import TCPServer
from RequeteJSON import RequeteJSON
import time
monServer = TCPServer()
print monServer.connectionEstablished
command = input('Enter your command')
print command
parameter = input('Enter parameter or press enter if no parameter needed')
print parameter
myRequest = RequeteJSON(command,parameter)
monServer.sendFile('data.json')
monServer.closeConnection()
