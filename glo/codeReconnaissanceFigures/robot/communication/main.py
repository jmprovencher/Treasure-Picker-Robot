from UARTDriver import UARTDriver
from TCPClient import TCPClient
monClient = TCPClient()
data = monClient.receiveFile()
print data
#monUart = UARTDriver('COM8', 9600)