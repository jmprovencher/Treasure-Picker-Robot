import socket

class Server:
  def __init__(self):
    port = 60000                    
    self.s = socket.socket()             
    host = socket.gethostname()    
    hostAdress = socket.gethostbyname(host)
    print hostAdress
    self.s.bind((host, port))           
    self.s.listen(5)                    
    print 'Server listening....'
    self._establishConnection()

  def _establishConnection(self):
    while True:
      print 'hello'
      conn, addr = self.s.accept()     # Establish connection with client.
      print 'Got connection from', addr
      data = conn.recv(1024)
      print('Server received', repr(data))
