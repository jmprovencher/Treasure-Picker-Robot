from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from robot.communication.LectureUART import LectureUART
from threading import Thread
import time
from robot.communication.ObtenirTension import ObtenirTension
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
        self.pretEnvoyerIndice = False

        self.lettreObtenue = None
        self.indiceObtenu = None
        self.adresseIP = '192.168.0.45'
        self.tensionCondensateur = 0

        self._demarrerLectureUART()
        self._demarrerConnectionTCP()
        self._demarrerFeedVideo()

    def run(self):
        self.uartDriver.phaseInitialisation()

    def demarrerAlignementStation(self):
        self.alignementEnCours = True
        self.uartDriver.cameraPositionFace()
        self.threadVideo.demarrerCapture()

        self._demarrerAnalyseVideo('station')

        self.uartDriver.preAlignementStation()
        self._executerAlignement()
        self._attendreChargeComplete()
        self._decoderManchester()
        self.uartDriver.postAlignementStation()

        self.alignementEnCours = False
        self.threadVideo.suspendreCapture()

    def demarrerAlignementTresor(self):
        self.alignementEnCours = True
        self.uartDriver.cameraPositionTresor()
        self.threadVideo.demarrerCapture()

        self._demarrerAnalyseVideo('tresor')

        self.uartDriver.preAlignementTresor()
        self._executerAlignement()
        self.uartDriver.postAlignementTresor()

        self.alignementEnCours = False
        self.threadVideo.suspendreCapture()

    def demarrerAlignementIle(self):
        self.alignementEnCours = True
        self.uartDriver.cameraPositionDepot()

        # Implementer le traitement de nimporte quelle forme
        self._demarrerAnalyseVideo('bleu')

        self._executerAlignement()
        self.uartDriver.postAlignementIle()

        self.alignementEnCours = False
        self.threadVideo.suspendreCapture()

    def ajouterDirectives(self, instructions):
        self.instructions.append(instructions)

    def traiterCommande(self, commande, parametre):
        if (commande == 'alignement_ile'):
            self.demarrerAlignementIle()
        elif (commande == 'alignement_tresor'):
            self.demarrerAlignementTresor()
        elif (commande == 'alignement_station'):
            self.demarrerAlignementStation()
        else:
            self.uartDriver.sendCommand(commande, parametre)

    def _executerAlignement(self):
        for inst in self.instructions:
            self.commandeTerminee = False
            commande, parametre = inst
            self.uartDriver.sendCommand(commande, parametre)
            time.sleep(2)
            self.commandeTerminee = True

    def _decoderManchester(self):
        self.uartDriver.lireManchester()
        self._attendreReceptionLettre()
        cible = self.service.obtenirCible(self.lettreObtenue)

    def _attendreReceptionLettre(self):
        while (self.lettreObtenue is None):
            print("Waiting for Manchester...")
            time.sleep(2)
        print("Lettre recu par le robot : %s" % self.lettreObtenue)
        self.pretEnvoyerLettre = True

    def _attendreChargeComplete(self):
        while (float(self.tensionCondensateur) < 4.60):
            time.sleep(0.5)
        self.uartDriver.stopCondensateur()

    def _demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.start()

    def _demarrerConnectionTCP(self):
        self.robotClient = RobotClient(self, self.adresseIP)
        self.robotClient.start()

    def _demarrerLectureUART(self):
        self.threadLecture = LectureUART(self)
        self.threadLecture.start()

    def _demarrerAnalyseVideo(self, type):
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self, type)
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

    def _demarrerObtenirTension(self):
        self.obtenirTension = ObtenirTension(self)
        self.obtenirTension.start()