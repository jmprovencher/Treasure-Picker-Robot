from UARTDriver import UARTDriver
from TCPClient import TCPClient
monClient = TCPClient()
monUart = UARTDriver('COM8', 9600) #on Windows
#monUart = UARTDriver('/dev/ttyACM0', 9600) #on linux

while 1:
        while 1:
            try:
                data = monClient.receiveFile()
                break
            except:
                print "Connection Lost, Trying to reconnect"
                monClient = TCPClient()

        if data == -1:
            print('Error while receiving file')
        else:
            print data
            commande = data['commande']
            parametre = data['parametre']
            monUart.sendCommand(commande, parametre)