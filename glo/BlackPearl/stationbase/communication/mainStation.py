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
        parameter = ''
        if command == 'forward' or command == 'backward' or command == 'left' or command == 'right':
            while True:
                try:
                    parameter = input('Enter parameter: ')
                    if type(parameter) == int:
                        break

                except:
                    print 'Error: Parameter must be a number!'
        else:
            parameter = ''
        myRequest = RequeteJSON(command, parameter)
        while 1:
            try:
                monServer.sendFile('data.json')
            except:
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                monServer.closeConnection()
                monServer = TCPServer()
                print monServer.connectionEstablished
            else:
                break

