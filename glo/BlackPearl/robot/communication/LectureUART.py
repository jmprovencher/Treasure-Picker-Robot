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
            self.analyserLecture(info)
            print "Lecture UART: "
            print info


    def analyserLecture(self, info):
        lettre_manchester = info[0]
        if (info.count(lettre_manchester) == 4):
            self.robot.lettreObtenue = lettre_manchester
            print("Lettre obtenue : %s" %lettre_manchester)
        elif (info == 'done'):
            print("AnalyserLecture: Commande est terminee")
            self.robot.commandeTerminee = True
        else:
            self.robot.tensionCondensateur = info
            print("Nouvelle tension :", info)
