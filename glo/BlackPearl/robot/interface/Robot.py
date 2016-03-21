# import the necessary packages
from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from threading import Thread, RLock

verrou = RLock()

class Robot(Thread):
    def __init__(self, uartDriver):
        Thread.__init__(self)
        print("Init")
        self.uartDriver = uartDriver
        self.alignementTresor = False
        self.alignementDepot = False
        self.positionTresor = False
        self.positionDepot = False
        self.demarrerConnectionTCP()
        self.threadVideo = FeedVideoRobot()
        self.analyseImageEmbarquee = AnalyseImageEmbarquee()

    def run(self):
        print("UIuu")

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement'):
            self.demarrerPhaseAlignement(parametre)
        else:
            self.uartDriver.sendCommand(commande, parametre)

    def demarrerPhaseAlignement(self, typeAlignement):
        self.initialiserVideo()
        if (typeAlignement == "depot"):
            self.alignementDepot = True
        else:
            self.alignementTresor = True
        self.analyseImageEmbarquee.start()

    def demarrerConnectionTCP(self):
        self.robotClient = RobotClient(self)
        self.robotClient.start()

    def initialiserVideo(self):
        self.threadVideo.start()