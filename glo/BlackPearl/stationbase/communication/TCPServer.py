import socket


class TCPServer:
    def __init__(self):
        port = 60000
        self.s = socket.socket()
        host = socket.gethostname()
        hostAddress = socket.gethostbyname(host)
        print ('Server address : '+hostAddress)
        self.s.bind((host, port))
        self.s.listen(0)
        print 'Server listening....'
        self.conn = self._establishConnection()
        self.connectionEstablished = True

    def _establishConnection(self):
        conn, addr = self.s.accept()  # Establish connection with client.
        print 'Got connection from', addr
        return conn

    def sendFile(self, filename):
        f = open(filename, 'r')
        data = f.read()
        while data:
            self.conn.send(data)
            print('Sent ', repr(data))
            data = f.read()
        f.close()
        print('Done sending file')
        return 1

    def closeConnection(self):
        self.conn.close()
        print 'Connection closed'

