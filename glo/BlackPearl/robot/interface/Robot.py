from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from robot.communication.LectureUART import LectureUART
from threading import Thread
import time
# from robot.communication.ObtenirTension import ObtenirTension
from robot.interface.RobotService import RobotService


class Robot(Thread):
    def __init__(self, uartDriver):
        Thread.__init__(self)
        self.uartDriver = uartDriver
        self.service = RobotService()
        self.instructions = []

        self.alignementEnCours = False
        self.positionTresor = False
        self.positionDepot = False
        self.tacheTerminee = False
        self.commandeTerminee = False
        self.pretEnvoyerLettre = False

        self.lettreObtenue = None
        self.indiceObtenu = None
        # self.adresseIP = '192.168.0.45'
        self.adresseIP = '10.248.39.53'
        self.tensionCondensateur = 0
        self._demarrerFeedVideo()
        self._demarrerConnectionTCP()
        self._demarrerLectureUART()


    def run(self):
        print("Run")
        self.robotClient.demarrageTermine = True
        #self.uartDriver.phaseInitialisation()


    def demarrerAlignementStation(self):
        print("Demarre phase alignement station")
        self.alignementEnCours = True
        self.uartDriver.cameraPositionFace()
        self.threadVideo.demarrerCapture()

        self._demarrerAnalyseVideo('station')

        self.uartDriver.preAlignementStation()
        self._executerAlignement()
        self._attendreChargeComplete()
        print("Charge complete")
        self.uartDriver.stopCondensateur()
        print("CONDENSATEUR OFF")
        self.uartDriver.sendCommand('backward', 10)
        time.sleep(5)
        self._decoderManchester()
        self.uartDriver.postAlignementStation()

        self.alignementEnCours = False

    def demarrerAlignementTresor(self):
        print("Demarre phase alignement tresor")
        self.alignementEnCours = True
        self.uartDriver.cameraPositionDepot()
        self.threadVideo.demarrerCapture()

        self._demarrerAnalyseVideo('tresor')

        self.uartDriver.preAlignementTresor()
        self.uartDriver.cameraPositionFace()
        self._executerAlignement()
        self.uartDriver.postAlignementTresor()

        self.alignementEnCours = False

    def demarrerAlignementIle(self, parametre):
        print("Demarre phase alignement ile")
        self.alignementEnCours = True
        self.uartDriver.cameraPositionDepot()

        # Implementer le traitement de nimporte quelle forme
        self._demarrerAnalyseVideo(parametre)

        self._executerAlignement()
        self.uartDriver.postAlignementIle()

        self.alignementEnCours = False

    def ajouterDirectives(self, instructions):
        self.instructions.append(instructions)

    def traiterCommande(self, commande, parametre):
        if commande == 'alignement_ile':
            self.demarrerAlignementIle(parametre)
        elif commande == 'alignement_tresor':
            self.demarrerAlignementTresor()
        elif commande == 'alignement_station':
            self.demarrerAlignementStation()
        elif commande == "decoderManchester":
            self._decoderManchester()
        else:
            self.uartDriver.sendCommand(commande, parametre)
            self.attendreCommandeTerminee()

    def _executerAlignement(self):
        for inst in self.instructions:
            commande, parametre = inst
            parametre = int(parametre)
            self.commandeTerminee == False
            self.uartDriver.sendCommand(commande, parametre)
            print("Commande executee:")
            print(commande, parametre)
            self.attendreCommandeTerminee()

    def attendreCommandeTerminee(self):
        while not self.commandeTerminee:
            print("Attente commande terminee")
            time.sleep(0.5)

    def _decoderManchester(self):
        self.uartDriver.lireManchester()

    def _attendreChargeComplete(self):
        while (float(self.tensionCondensateur) < 4.60):
            print(self.tensionCondensateur)
            self.robotClient.envoyerTension()
            time.sleep(0.5)

    def _demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.initialiserVideo()
        self.threadVideo.start()

    def _demarrerConnectionTCP(self):
        self.robotClient = RobotClient(self, self.adresseIP)
        self.robotClient.start()

    def _demarrerLectureUART(self):
        self.threadLecture = LectureUART(self)
        self.threadLecture.start()

    def _demarrerAnalyseVideo(self, type):
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self)
        self.analyseImageEmbarquee.definirType(type)
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()
        # self.threadVideo.suspendreCapture()

