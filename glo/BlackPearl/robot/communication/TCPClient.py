import socket
import json

class TCPClient:
    def __init__(self, adresseIP):
        self.s = socket.socket()
        self.port = 60000
        self.host = adresseIP
        #self.host = '192.168.1.25'
        #self.host = '192.168.1.37' #If on embedded computer in local network

    def _connectToServer(self):
        while True:
            try:
                self.s.connect((self.host, self.port))
                break
            except Exception as e:
                print("Connection failed with %s:%d. Exception is %s" % (self.host, self.port, e))
        return True

    def sendFile(self):
        print '\nsending file'
        f = open('data.json', 'r')
        data = f.read()
        while data:
            self.s.send(data)
            print('Sent: ', repr(data))
            data = f.read()
        f.close()
        print('Done sending file')
        return 1

    def receiveFile(self):
        print('\nreceiving data...')
        data = self.s.recv(1024)
        print 'fichier recu.'
        jsonObject = json.loads(data)
        print('data successfully decoded')
        return jsonObject

    def closeConnection(self):
        self.s.close()
        print('Closed Connection with Base Station')


