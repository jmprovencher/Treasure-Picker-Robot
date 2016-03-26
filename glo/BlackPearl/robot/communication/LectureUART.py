from threading import Thread, RLock
import time

verrou = RLock()

class LectureUART(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot

    def run(self):
        while 1:
            info = self.robot.uartDriver.UART.read(1) #TODO: Pas sur du type reçu...
            if (info == '???'): #TODO: Avec quoi comparer lorsque la commande est termine
                self.robot.commandeTerminee = True
            else:
                self.robot.tensionCondensateur = info #TODO: Pas sur du type de info...
