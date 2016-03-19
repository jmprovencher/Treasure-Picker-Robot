import socket
from threading import Thread, RLock
import time

verrou = RLock()

class TCPServer(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.creeConnection()
        self.connection = self._establishConnection()

    def run(self):
        while 1:
            if (self.doitEnvoyerFichier()):
                self.sendFile(self, 'data.json')
                self.stationBase.envoyerFichier = False
            time.sleep(1)

    def doitEnvoyerFichier(self):
        with verrou:
            return self.stationBase.envoyerFichier
        
    def creeConnection(self):
        print '\ncreation connection TCP'
        port = 60000
        self.s = socket.socket()
        host = socket.gethostname()
        hostAddress = socket.gethostbyname(host)
        print hostAddress
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

