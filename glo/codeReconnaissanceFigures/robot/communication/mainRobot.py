from UARTDriver import UARTDriver
from TCPClient import TCPClient
monClient = TCPClient()
#monUart = UARTDriver('COM8', 9600)

while 1:
        data = monClient.receiveFile()
        print data
        commande = data['commande']
        parametre = data['parametre']
    #monUart.sendCommand(commande, parametre)
