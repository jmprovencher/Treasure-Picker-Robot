import serial
import time

COMMANDE_FORWARD = 'forward'
COMMANDE_BACKWARD = 'backward'
COMMANDE_LEFT = 'left'
COMMANDE_RIGHT = 'right'
COMMANDE_LEFT_P = 'leftP'
COMMANDE_RIGHT_P = 'rightP'
COMMANDE_PICKUP = 'pickup'
COMMANDE_DROP = 'drop'
COMMANDE_CHARGE_CONDENSATEUR = 'chargeCondensateur'
COMMANDE_STOP_CONDENSATEUR = 'stopCondensateur'
COMMANDE_ROTATE_CLOCKWISE = 'rotateClockwise'
COMMANDE_ROTATE_ANTI_CLOCKWISE = 'rotateAntiClockwise'
COMMANDE_CAMERA_RIGHT = 'cameraRight'
COMMANDE_CAMERA_LEFT = 'cameraLeft'
COMMANDE_CAMERA_FRONT = 'cameraFront'
COMMANDE_CAMERA_TREASURE = 'cameraTreasure'
COMMANDE_READ_MANCHESTER = 'readManchester'
COMMANDE_CHECK_CAPACITY = 'checkCapacity'


class UARTDriver:
    def __init__(self, comPort, baudRate):
        self.comPort = comPort
        self.baudRate = baudRate
        self.UART = self._initializeUARTCom(self.comPort, self.baudRate)

    def _initializeUARTCom(self, comPort, baudRate):
        UART = serial.Serial(comPort, baudRate)
        time.sleep(2)
        return UART

    def phaseInitialisation(self):
        self.monterPrehenseur()
        time.sleep(2)
        self.cameraPositionDepot()
        time.sleep(0.2)
        self.cameraPositionFace()

    def cameraPositionDepot(self):
        self.UART.write(b'x'.encode())
        time.sleep(0.5)

    def cameraPositionFace(self):
        self.UART.write(b'c'.encode())
        time.sleep(0.5)

    def cameraPositionTresor(self):
        self.UART.write(b'd'.encode())

    def cameraDescendre(self):
        self.UART.write(b'y'.encode())

    def descendrePrehenseur(self):
        self.UART.write(b'P'.encode())

    def monterPrehenseur(self):
        self.UART.write(b'Q'.encode())

    def brasserPrehenseur(self):
        self.UART.write(b'R'.encode())

    def activerAimant(self):
        self.UART.write(b'g'.encode())

    def desactiverAimant(self):
        self.UART.write(b'h'.encode())

    def preAlignementTresor(self):
        self.descendrePrehenseur()
        time.sleep(4)
        self.activerAimant()
        time.sleep(0.5)

    def preAlignementStation(self):
        self.chargerCondensateur()
        time.sleep(1)

    def postAlignementTresor(self):
        time.sleep(1)
        self.sendCommand('backward', 6)
        time.sleep(2)
        self.monterPrehenseur()
        time.sleep(4)
        self.desactiverAimant()
        time.sleep(2)

    def postAlignementStation(self):
        self.sendCommand('rotateAntiClockwise', 90)
        time.sleep(1)


    def postAlignementIle(self):
        self.activerAimant()
        time.sleep(1)
        self.descendrePrehenseur()
        time.sleep(3)
        self.desactiverAimant()
        time.sleep(6)
        self.brasserPrehenseur()
        time.sleep(2)
        self.monterPrehenseur()
        time.sleep(2)
        self.sendCommand('backward', 5)
        time.sleep(3)
        self.executionTerminee()

    def chargerCondensateur(self):
        self.sendCommand('chargeCondensateur', 0)

    def stopCondensateur(self):
        self.sendCommand('stopCondensateur', 0)

    def lireManchester(self):
        self.sendCommand('readManchester', 0)
        print("Commande readManchester envoyee au UART")

    def executionTerminee(self):
        for j in range(0, 6):
            self.cameraPositionFace()
            time.sleep(0.1)
            self.cameraPositionDepot()
            time.sleep(0.1)

    def sendCommand(self, command, parameter):
        parameter = chr(parameter)

        if command == COMMANDE_FORWARD:
            self.UART.write(b'8'.encode())
            self.UART.write(parameter)

        elif command == COMMANDE_BACKWARD:
            self.UART.write(b'2'.encode())
            self.UART.write(str(parameter).encode())

        elif command == COMMANDE_LEFT:
            self.UART.write(b'4'.encode())
            self.UART.write(str(parameter).encode())

        elif command == COMMANDE_RIGHT:
            self.UART.write(b'6'.encode())
            self.UART.write(str(parameter).encode())

        elif command == COMMANDE_LEFT_P:
            self.UART.write(b'1'.encode())
            self.UART.write(str(parameter).encode())

        elif command == COMMANDE_RIGHT_P:
            self.UART.write(b'3'.encode())
            self.UART.write(str(parameter).encode())

        elif command == COMMANDE_PICKUP:
            self.UART.write(b'g'.encode())

        elif command == COMMANDE_DROP:
            self.UART.write(b'h'.encode())

        elif command == COMMANDE_CHARGE_CONDENSATEUR:
            self.UART.write(b'e'.encode())

        elif command == COMMANDE_STOP_CONDENSATEUR:
            self.UART.write(b'f'.encode())

        elif command == COMMANDE_ROTATE_CLOCKWISE:
            self.UART.write(b'9'.encode())
            self.UART.write(parameter)

        elif command == COMMANDE_ROTATE_ANTI_CLOCKWISE:
            self.UART.write(b'7'.encode())
            self.UART.write(parameter)

        elif command == COMMANDE_CAMERA_RIGHT:
            self.UART.write(b'a'.encode())

        elif command == COMMANDE_CAMERA_LEFT:
            self.UART.write(b'b'.encode())

        elif command == COMMANDE_CAMERA_FRONT:
            self.UART.write(b'c'.encode())

        elif command == COMMANDE_CAMERA_TREASURE:
            self.UART.write(b'd'.encode())

        elif command == COMMANDE_READ_MANCHESTER:
            self.UART.write(b'z'.encode())

        elif command == COMMANDE_CHECK_CAPACITY:
            self.UART.write(b'k'.encode())

        return 1
