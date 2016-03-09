from TCPServer import TCPServer
import time
monServer = TCPServer()
print monServer.connectionEstablished
monServer.sendFile('data.json')
monServer.closeConnection()
