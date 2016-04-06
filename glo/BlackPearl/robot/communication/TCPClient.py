import socket
import json
import time


class TCPClient:
    def __init__(self, adresseIP):
        self.s = socket.socket()
        self.port = 60000
        self.host = adresseIP

    def _connectToServer(self):
        while True:
            try:
                self.s.connect((self.host, self.port))
                break
            except Exception as e:
                print("Connection impossible avec %s:%d. Erreur %s" % (self.host, self.port, e))
                time.sleep(5)
        return True

    def sendFile(self):
        f = open('data.json', 'r')
        data = f.read()
        while data:
            print("Commande JSON:")
            print(data)
            self.s.send(data)
            data = f.read()
        f.close()
        return 1

    def receiveFile(self):
        data = self.s.recv(1024)
        print("Data received: %s" %data)
        jsonObject = json.loads(data)
        return jsonObject

    def closeConnection(self):
        self.s.close()
        print('Connection avec Station de Base terminee')
