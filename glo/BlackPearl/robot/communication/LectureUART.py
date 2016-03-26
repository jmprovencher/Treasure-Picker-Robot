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
            if (info == 'done'):
                self.robot.commandeTerminee = True
            elif (info == 'pret'):
                self.robot.robotPret = True
            else:
                self.robot.tensionCondensateur = info
