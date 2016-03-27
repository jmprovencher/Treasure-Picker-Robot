import socket
from threading import Thread, RLock
import time
import json

class TCPServer():
    def __init__(self):
        self.creeConnection()
        self.connection = self._establishConnection()
        
    def creeConnection(self):
        print '\n-------------------------------------------------------------'
        print 'Creation connection TCP'
        print '-------------------------------------------------------------\n'
        port = 60000
        self.s = socket.socket()
        host = socket.gethostname()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        hostAddress = self.get_address(host)
        print 'adresse serveur: '+hostAddress
        self.s.bind((hostAddress, port))
        self.s.listen(5)
        print 'le serveur ecoute...'

    def _establishConnection(self):
        conn, addr = self.s.accept()  # Establish connection with client.
        print 'connection a l''adresse: ', addr
        return conn

    def sendFile(self, data):
        print '\nEssaye d''envoyer une requete au robot...'
        f = open('data.json', 'r')
        data = f.read()
        while data:
            self.s.send(data)
            print('Sent: ', repr(data))
            data = f.read()
        f.close()
        print 'Envoie reussi.'
        return 1

    def receiveFile(self):
        print('\nEn attente de requete...')
        data = self.connection.recv(1024)
        jsonObject = json.loads(data)
        print('requete recu.')
        print 'requete: ', repr(data)
        return jsonObject

    def closeConnection(self):
        self.connection.close()
        print '\nConnection fermee'

    def get_address(self, host):
        address = socket.gethostbyname(host)
        if not address or address.startswith('127.'):
            tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tmp.connect(('4.2.2.1', 0))
            address = tmp.getsockname()[0]
            tmp.close()
        return  address

