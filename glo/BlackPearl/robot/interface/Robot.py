# import the necessary packages
from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from robot.communication.LectureUART import LectureUART
from threading import Thread, RLock
import time

verrou = RLock()

class Robot(Thread):
    def __init__(self, uartDriver):
        Thread.__init__(self)
        print("Robot init")
        self.uartDriver = uartDriver
        self.instructions = []
        self.alignement = False
        self.alignementDepot = False
        self.positionTresor = False
        self.positionDepot = False
        self.tacheTerminee = False
        self.commandeTerminee = False
        self.tensionCondensateur = 0
        self.demarrerConnectionTCP()
        self.demarrerLectureUART()

    def run(self):
        print("Robot run")

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        print("Demarre TCP Client")
        self.robotClient = RobotClient(self)
        self.robotClient.start()

    def demarrerLectureUART(self):
        print "Demarer lecture UART"
        self.threadLecture = LectureUART(self)
        self.threadLecture.start()

    def demarrerAlignement(self, typeAlignement):
        self.demarrerFeedVideo()
        self.alignement = True
        if (typeAlignement == "0"):
            self.alignementStation = True
            #self.uartDriver.cameraPositionTresor()
        if (typeAlignement == "1"):
            self.alignementTresor = True
            self.uartDriver.cameraPositionTresor()
            while not (self.commandeTerminee):
                time.sleep(1)
            self.uartDriver.descendrePrehenseur()
        elif (typeAlignement == "2"):
            self.alignementDepot = True
            self.uartDriver.descendrePrehenseur()
            while not (self.commandeTerminee):
                time.sleep(1)
            self.uartDriver.cameraPositionDepot()

        time.sleep(2)
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self)
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()
        print("Envoie les commandes d'ajustements (FROM ROBOT)")
        self.effectuerAlignement()

    def effectuerAlignement(self):
        for inst in self.instructions:
            print("Envoie instruction alignement au UART")
            self.uartDriver.sendCommand(inst)
            while not (self.commandeTerminee):
                time.sleep(0.5)
            self.commandeTerminee = True
        self.alignement = False

    def ajouterCommande(self, instructions):
        self.instructions.append(instructions)

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement'):
            print("Commence phase alignement: %s", parametre)
            self.demarrerAlignement(parametre)
        else:
            self.uartDriver.sendCommand(commande, parametre)
            print("Commande envoye au UART")
