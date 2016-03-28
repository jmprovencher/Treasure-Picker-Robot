from TCPServer import TCPServer
from RequeteJSON import RequeteJSON
import time
monServer = TCPServer()
while 1:
    command = raw_input('Enter your command: ')
    if command == 'exit':
        monServer.closeConnection()

    else:
        parameter = ''
        if command == 'forward' or command == 'backward' or command == 'left' or command == 'right' or command =='rotateClockwise' or command =='rotateAntiClockwise':
            parameter = input('Enter parameter: ')
            parameter = int(parameter)
            print parameter
        else:
            parameter = ''
        myRequest = RequeteJSON(command, parameter)
        while 1:
            try:
                monServer.sendFile()
            except:
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                monServer.closeConnection()
                monServer = TCPServer()
            else:
                break

