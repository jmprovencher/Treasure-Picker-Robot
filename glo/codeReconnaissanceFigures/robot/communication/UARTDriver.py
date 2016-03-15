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

        if command == 'forward':
            self.UART.write(b'8'.encode())
            self.UART.write(b'parameter'.encode())

        elif command == 'backward':
            self.UART.write(b'2'.encode())
            self.UART.write(parameter.encode())

        elif command == 'left':
            self.UART.write(b'4'.encode())
            self.UART.write(parameter.encode())

        elif command == 'right':
            self.UART.write(b'6'.encode())
            self.UART.write(parameter.encode())

        elif command == 'armUp':
            pass

        elif command == 'armDown':
            pass

        elif command == 'magnetOn':
            pass

        elif command == 'magnetOff':
            pass

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
