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
        self.uartDriver = uartDriver
        self.instructions = []
        self.alignementEnCours = False
        self.alignementDepot = False
        self.positionTresor = False
        self.positionDepot = False
        self.tacheTerminee = False
        self.commandeTerminee = False
        self.tensionCondensateur = 0
        self.demarrerConnectionTCP()
        self.demarrerLectureUART()

    def run(self):
        print("Robot initialized")

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        print("Demarre TCP Client")
        self.robotClient = RobotClient(self)
        self.robotClient.start()

    def demarrerLectureUART(self):
        print "Demarrer lecture UART"
        self.threadLecture = LectureUART(self)
        self.threadLecture.start()

    def demarrerAlignementIle(self):
        self.demarrerFeedVideo()
        self.alignementEnCours = True
        self.uartDriver.descendrePrehenseur()
        print("Decendre prehenseur")
        self.uartDriver.sendCommand('drop', 0)
        
        while not (self.commandeTerminee):
            print("If this prints, this is useful")
            time.sleep(1)

        self.uartDriver.cameraPositionDepot()
        print("######### CAMERA DOWN #########")
        time.sleep(2)

        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self, 'bleu')
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

        self.executerAlignement()
        time.sleep(0.5)
        print("######### COMMENCE AUTO PILOT #########")
        self.uartDriver.postAlignementIle()
        print("======== ALIGNEMENT TERMINER ========")
        self.alignementEnCours = False

    def demarrerAlignementTresor(self):
        self.demarrerFeedVideo()
        self.alignementEnCours = True
        self.uartDriver.descendrePrehenseur()
        while not (self.commandeTerminee):
            print("If this prints, this is useful")
            time.sleep(1)
        self.uartDriver.cameraPositionDepot()
        print("######### Camera and Arm DOWN #########")
        time.sleep(2)

        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self, 'tresor')
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

        self.executerAlignement()
        time.sleep(0.5)
        print("######### COMMENCE AUTO PILOT #########")
        self.uartDriver.postAlignementTresor()
        print("======== ALIGNEMENT TERMINER ========")
        self.alignementEnCours = False

    def executerAlignement(self):
        for inst in self.instructions:
            self.commandeTerminee = False
            self.uartDriver.sendCommand(inst)
            print("Commande envoyee: %s" % inst)
            while not (self.commandeTerminee):
                print("Commande en cours execution")
                time.sleep(0.5)
            print("Commande effectuee")
            self.commandeTerminee = True

    def ajouterDirectives(self, instructions):
        self.instructions.append(instructions)

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement_ile'):
            print("Commence phase alignement: %s" % parametre)
            self.demarrerAlignementIle()
        elif (commande == 'aligenemt_tresor'):
            print("Commence phase alignement: %s" % parametre)
            self.demarrerAlignementTresor()
        else:
            self.uartDriver.sendCommand(commande, parametre)
            print("Commande envoye au UART")
