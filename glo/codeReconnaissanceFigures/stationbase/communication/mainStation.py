from TCPServer import TCPServer
from RequeteJSON import RequeteJSON
import time
monServer = TCPServer()
print monServer.connectionEstablished
while 1:
    command = raw_input('Enter your command: ')
    if command == 'exit':
        monServer.closeConnection()
    else:
        print command
        if command == 'forward' or command == 'backward' or command == 'left' or command == 'right':
            while True:
                try:
                    parameter = input('Enter parameter or press enter if no parameter needed')
                    if type(parameter) == int:
                        break

                except:
                    print 'Error: Parameter must be a number!'
            print parameter
        else:
            parameter = ''
        myRequest = RequeteJSON(command, parameter)
        monServer.sendFile('data.json')

