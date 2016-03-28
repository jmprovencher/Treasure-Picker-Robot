from threading import Thread, RLock
import time
import struct

verrou = RLock()

class LectureUART(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
	print "Charlo Suck a linit"

    def run(self):
        while 1:
	    print "Charlo suck"
            info = self.robot.uartDriver.UART.read(4)
	    print "Lecture UART: "
	    print info
            if (info == 'done'):
                self.robot.commandeTerminee = True
            else:
                self.robot.tensionCondensateur = info
