from threading import Thread, RLock
import time
import struct

verrou = RLock()

class LectureUART(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot

    def run(self):
        while 1:
            info = self.robot.uartDriver.UART.read(4)
            info = struct.unpack('f', info)
            if (info == 10.0):
                self.robot.commandeTerminee = True
            elif (info == 20.0):
                self.robot.robotPret = True
            else:
                self.robot.tensionCondensateur = info
