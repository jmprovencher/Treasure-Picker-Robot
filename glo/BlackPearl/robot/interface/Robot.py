# import the necessary packages
from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from threading import Thread, RLock
import time

verrou = RLock()

class Robot(Thread):
    def __init__(self, uartDriver):
        Thread.__init__(self)
        print("Robot init")
        self.uartDriver = uartDriver
        self.instructions = []
        self.robotPret = False
        self.alignementTresor = False
        self.alignementDepot = False
        self.positionTresor = False
        self.positionDepot = False
        self.tacheTerminee = False
        self.commandeTerminee = False
        self.tensionCondensateur = 0
        self.demarrerConnectionTCP()
        self.demarrerLectureUART()
        #self.demarrerAlignement('tresor')

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

    def demarrerAlignement(self, typeAlignement):
        #self.demarrerFeedVideo()
        if (typeAlignement == "depot"):
            self.alignementDepot = True
            #self.uartDriver.cameraPositionDepot()
        if (typeAlignement == "tresor"):
            self.alignementTresor = True
            #self.uartDriver.cameraPositionTresor()

        time.sleep(2)
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self)
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()
        print("Envoie les commandes d'ajustements (FROM ROBOT)")
        self.effectuerAlignement()

    def effectuerAlignement(self):
        for inst in self.instructions:
            print("Envoie instruction alignement au UART")
            #self.uartDriver.sendCommand(inst)
            #Attendre que la commande soit faite, trouver autre moyen plus tard
            time.sleep(2)

    def ajouterCommande(self, instructions):
        self.instructions.append(instructions)

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement'):
            print("Commence phase alignement: %s", parametre)
            self.demarrerAlignement(parametre)
        else:
            self.uartDriver.sendCommand(commande, parametre)
            print("Commande envoye au UART")
