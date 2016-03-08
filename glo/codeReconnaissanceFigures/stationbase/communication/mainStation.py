from TCPServer import TCPServer
monServer = TCPServer()
print monServer.connectionEstablished
monServer.sendFile('data.json')
