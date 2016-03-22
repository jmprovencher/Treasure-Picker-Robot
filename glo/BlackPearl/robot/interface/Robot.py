# import the necessary packages
from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from threading import Thread, RLock
import time

verrou = RLock()

class Robot(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("Robot init")
        #self.uartDriver = uartDriver
        self.alignementTresor = False
        self.alignementDepot = False
        self.positionTresor = False
        self.positionDepot = False
        self.tacheTerminee = False
        self.demarrerConnectionTCP()

    def run(self):
        print("Robot run")
        #if(self.tacheTerminee):


    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        print("Demarre TCP Client")
        self.robotClient = RobotClient(self)
        self.robotClient.start()

    def demarrerPhaseAlignement(self, typeAlignement):
        self.demarrerFeedVideo()
        time.sleep(2)
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self)
        if (typeAlignement == "depot"):
            self.alignementDepot = True
        else:
            self.alignementTresor = True

        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement'):
            print("Commence phase alignement: %s", parametre)
            self.demarrerPhaseAlignement(parametre)
        else:
            print("Commande directe")
            #self.uartDriver.sendCommand(commande, parametre)

