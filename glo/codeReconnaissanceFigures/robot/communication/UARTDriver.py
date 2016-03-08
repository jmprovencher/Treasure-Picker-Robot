import serial
import time


class UARTDriver:
    def __init__(self, comPort, baudRate):
        self.comPort = comPort
        self.baudRate = baudRate
        self.UART = self._initializeUARTCom(self.comPort, self.baudRate)

    def _initializeUARTCom(self, comPort, baudRate):
        UART = serial.Serial(comPort, baudRate)
        time.sleep(2)  # the sleep time is important to make sure we don't send any messages before the initialization is complete
        return UART

    def sendCommand(self, command, parameter):

        if command == 'avancer':
            self.UART.write(b'8'.encode())
            self.UART.write(b'parameter'.encode())

        elif command == 'reculer':
            self.UART.write(b'2'.encode())
            self.UART.write(parameter.encode())

        elif command == 'gauche':
            self.UART.write(b'4'.encode())
            self.UART.write(parameter.encode())

        elif command == 'droite':
            self.UART.write(b'6'.encode())
            self.UART.write( parameter.encode())

        commandComplete = self.UART.read(2)
        return commandComplete
