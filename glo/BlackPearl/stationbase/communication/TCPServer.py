import socket
import ConfigPath
import json


class TCPServer:
    def __init__(self):
        self.s = None
        self.creeConnection()
        self.connection = None
        
    def creeConnection(self):
        print '\n-------------------------------------------------------------'
        print 'Creation connection TCP'
        print '-------------------------------------------------------------\n'
        port = 60000
        self.s = socket.socket()
        host = socket.gethostname()
        hostAddress = self.get_address(host)
        print 'adresse serveur: '+hostAddress
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((hostAddress, port))
        self.s.listen(5)
        print 'le serveur ecoute...'

    def establishConnection(self):
        connection, addr = self.s.accept()  # Establish connection with client.
        print 'connection a l''adresse: ', addr
        return connection

    def sendFile(self):
        print 'Essaye denvoyer une requete au robot...'
        f = open(ConfigPath.Config.appendToProjectPath('stationbase/communication/data.json'), 'r')
        data = f.read()
        while data:
            self.connection.send(data)
            print('Sent: ', repr(data))
            data = f.read()
        f.close()
        print 'Envoi reussi'
        return 1

    def receiveFile(self):
        print('\nEn attente de requete...')
        data = self.connection.recv(1024)
        print data
        print('requete recu.')
        while 1:
            try:
                jsonObject = json.loads(data)
                break
            except Exception as e:
                print e
        print 'requete decode.'
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
        return address

