import socket
import json


class TCPClient:
    def __init__(self):
        self.s = socket.socket()
        self.port = 60000
        self.hostTest = '10.248.251.245'
        self.host = '192.168.1.37' #If on embedded computer in local network
        self.connectionEstablished = self._connectToServer()

    def _connectToServer(self):
        while True:
            try:
                self.s.connect((self.hostTest, self.port))
                break
            except Exception as e:
                print("Connection failed with %s:%d. Exception is %s" % (self.hostTest, self.port, e))
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
        with open('received_file.json', 'wb') as f:
            print 'file opened'
            while True:
                print('receiving data...')
                data = self.s.recv(1024)
                print('data=%s', data)
                if not data:
                    break
                # write data to a file
                f.write(data)

        f.close()
        print('Successfully got the file')
        json_data = open('received_file.json').read()
        data = json.loads(json_data)
        commande = data['commande']
        parametre = data['parametre']
        print('Commande:', commande)
        print('Parametre:', parametre)
        return data


    def closeConnection(self):
        self.s.close()
        print('Closed Connection with Base Station')


