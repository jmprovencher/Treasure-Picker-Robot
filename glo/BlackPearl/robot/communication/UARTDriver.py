import serial
import time
import struct


class UARTDriver:
    def __init__(self, comPort, baudRate):
        self.comPort = comPort
        self.baudRate = baudRate
        self.UART = self._initializeUARTCom(self.comPort, self.baudRate)

    def _initializeUARTCom(self, comPort, baudRate):
        UART = serial.Serial(comPort, baudRate)
        time.sleep(2)  # the sleep time is important to make sure we don't send any messages before the initialization is complete
        return UART

    def cameraPositionDepot(self):
        self.UART.write(b'd'.encode())

    def cameraPositionTresor(self):
        self.UART.write(b'd'.encode())

    def descendrePrehenseur(self):
        self.UART.write(b'P'.encode())

    def monterPrehenseur(self):
        self.UART.write(b'Q'.encode())

    def activerAimant(self):
        self.UART.write(b'g'.encode())

    def desactiverAimant(self):
        self.UART.write(b'h'.encode())

    def postAlignementTresor(self):
        # Recule
        print("### BEEEEEEP BEEEEEEEEEEP ###")
        self.UART.write(b'2'.encode())
        self.UART.write(str('2').encode())
        print("### PREHENSEUR UP ###")
        self.monterPrehenseur()
        time.sleep(1)
        print("### MAGNET OFF ###")
        self.desactiverAimant()

    def postAlignementIle(self):
        print("### MAGNET ON ###")
        self.activerAimant()
        time.sleep(1)
        print("### PREHENSEUR DOWN ###")
        self.descendrePrehenseur()
        time.sleep(1)
        print("### MAGNET OFF ###")
        self.desactiverAimant()
        time.sleep(0.5)
        #Recule
        print("### BEEEEEEP BEEEEEEEEEEP ###")
        self.UART.write(b'2'.encode())
        self.UART.write(str('2').encode())

    def to_bytes(n, length, endianess='big'):
        h = '%x' % n
        s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
        return s if endianess == 'big' else s[::-1]

    def sendCommand(self, command, parameter):
        parameter = chr(parameter)

        if command == 'forward':
            self.UART.write(b'8'.encode())
            self.UART.write(parameter)

        elif command == 'backward':
            self.UART.write(b'2'.encode())
            self.UART.write(str(parameter).encode())

        elif command == 'left':
            self.UART.write(b'4'.encode())
            self.UART.write(str(parameter).encode())

        elif command == 'right':
            self.UART.write(b'6'.encode())
            self.UART.write(str(parameter).encode())

        elif command == 'pickup':
            self.UART.write(b'g'.encode())

        elif command == 'drop':
            self.UART.write(b'h'.encode())

        elif command == 'chargeCondensateur':
            self.UART.write(b'e'.encode())

        elif command == 'stopCondensateur':
            self.UART.write(b'f'.encode())

        elif command == 'rotateClockwise':
            self.UART.write(b'9'.encode())
            self.UART.write(parameter)

        elif command == 'rotateAntiClockwise':
            self.UART.write(b'7'.encode())
            self.UART.write(parameter)

        elif command == 'cameraRight':
            self.UART.write(b'a'.encode())

        elif command == 'cameraLeft':
            self.UART.write(b'b'.encode())

        elif command == 'cameraFront':
            self.UART.write(b'c'.encode())

        elif command == 'cameraTreasure':
            self.UART.write(b'd'.encode())

        #To implement when arduino will return command completion confirmation
        #commandComplete = self.UART.read(2)
        #return commandComplete
        return 1