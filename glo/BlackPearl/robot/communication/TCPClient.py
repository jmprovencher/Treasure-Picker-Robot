import socket
import json


class TCPClient:
    def __init__(self):
        self.s = socket.socket()
        self.port = 60000
        #self.host = '10.248.144.128'
        self.host = '127.0.1.1'
        #self.host = '192.168.1.37' #If on embedded computer in local network
        self.connectionEstablished = self._connectToServer()

    def _connectToServer(self):
        while True:
            try:
                self.s.connect((self.host, self.port))
                break
            except Exception as e:
                print("Connection failed with %s:%d. Exception is %s" % (self.host, self.port, e))
        return True

    def sendFile(self, filename,):
        f = open(filename, 'r')
        data = f.read()
        while data:
            self.s.send(data)
            print('Sent ', repr(data))
            data = f.read()
        f.close()
        print('Done sending file')
        return 1

    def receiveFile(self):
        print('receiving data...')
        data = self.s.recv(1024)
        jsonObject = json.loads(data)
        print('data successfully received')
        return jsonObject

    def closeConnection(self):
        self.s.close()
        print('Closed Connection with Base Station')


