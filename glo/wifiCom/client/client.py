import socket                
import json
import serial
import time
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.
print host
#s.connect(('192.168.1.37', port))
s.connect(('10.248.3.41', port))
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

json_data=open('received_file.json').read()

data = json.loads(json_data)
commande = data['commande']
parametre = data['parametre']
print('Commande:', commande)
print('Parametre:', parametre)


uart = serial.Serial('COM8', 9600) #initializing uart communication
time.sleep(2) #this sleep is important for initializing time
print(uart.name)

if(commande == 'avancer'): #
	
	uart.write(b'8'.encode())
	uart.write(b'2'.encode())


	uart.write(b'2'.encode())
	uart.write(b'2'.encode())

	uart.write(b'4'.encode())
	uart.write(b'2'.encode())

	uart.write(b'6'.encode())
	uart.write(b'2'.encode())



uart.close