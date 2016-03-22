import socket
from threading import Thread, RLock
import time

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
        self.s.listen(0)
        print '\nServeur ecoute'

    def _establishConnection(self):
        conn, addr = self.s.accept()  # Establish connection with client.
        print '\nconnection de: ', addr
        return conn

    def sendFile(self, filename):
        f = open(filename, 'r')
        data = f.read()
        while data:
            self.connection.send(data)
            print('\nSent ', repr(data))
            data = f.read()
        f.close()
        print('\nDone sending file')
        return 1

    def closeConnection(self):
        self.connection.close()
        print 'Connection closed'

    def get_address(self, host):
        address = socket.gethostbyname(host)
        if not address or address.startswith('127.'):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('4.2.2.1', 0))
            address = s.getsockname()[0]
        return address

