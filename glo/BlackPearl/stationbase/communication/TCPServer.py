import socket
from threading import Thread, RLock
import time
import json

class TCPServer():
    def __init__(self):
        self.creeConnection()
        self.connection = self._establishConnection()
        
    def creeConnection(self):
        print '\ncreation connection TCP'
        port = 60000
        self.s = socket.socket()
        host = socket.gethostname()
        hostAddress = self.get_address(host)
        print ('Server address : '+hostAddress)
        self.s.bind((host, port))
        self.s.listen(5)
        print '\nServeur ecoute'

    def _establishConnection(self):
        conn, addr = self.s.accept()  # Establish connection with client.
        print '\nconnection de: ', addr
        return conn

    def sendFile(self, filename):
        print '\nsending file'
        f = open(filename, 'r')
        data = f.read()
        while data:
            self.connection.send(data)
            print('Sent ', repr(data))
            data = f.read()
        f.close()
        print('Done sending file')
        return 1

    def receiveFile(self):
        print('\nreceiving data...')
        data = self.connection.recv(1024)
        jsonObject = json.loads(data)
        print('data successfully received')
        return jsonObject

    def closeConnection(self):
        self.connection.close()
        print 'Connection closed'

    def get_address(self, host):
        address = socket.gethostbyname(host)
        return address

