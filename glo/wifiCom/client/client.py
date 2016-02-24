import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.
print host
s.connect(('192.168.1.37', port))
s.send("Hello server!")	#if python 3, need to encode the string with bytes(string, 'utf-8')

with open('received_file.json', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully got the file')
s.close()