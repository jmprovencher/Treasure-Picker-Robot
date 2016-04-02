from threading import Thread, RLock
import time
import struct

verrou = RLock()

class ObtenirTension(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot

    def run(self):
        while 1:
            self.robot.uartDriver.sendCommand('checkCapacity', 0)
            time.sleep(5)


