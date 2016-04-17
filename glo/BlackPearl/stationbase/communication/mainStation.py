from TCPServer import TCPServer
from RequeteJSON import RequeteJSON
import time
monServer = TCPServer()

COMMANDE_EXIT = 'exit'
COMMANDE_FORWARD = 'forward'
COMMANDE_BACKWARD = 'backward'
COMMANDE_LEFT = 'left'
COMMANDE_RIGHT ='right'
COMMANDE_ROTATE_CLOCKWIZE = 'rotateClockwise'
COMMANDE_ROTATE_ANTI_CLOCKWIZE = 'rotateAntiClockwise'


while 1:
    command = raw_input('Enter your command: ')
    if command == COMMANDE_EXIT:
        monServer.closeConnection()

    else:
        parameter = ''
        if command == COMMANDE_FORWARD or command == COMMANDE_BACKWARD or command == COMMANDE_LEFT or command == COMMANDE_RIGHT or command == COMMANDE_ROTATE_CLOCKWIZE or command == COMMANDE_ROTATE_ANTI_CLOCKWIZE:
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
                print "Connection with the remote host lost, Trying to reconnect"
                monServer.closeConnection()
                monServer = TCPServer()
            else:
                break

