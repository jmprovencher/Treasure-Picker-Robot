# import the necessary packages
from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from robot.communication.LectureUART import LectureUART
from robot.communication.RequeteJSON import RequeteJSON
from robot.communication.islandServerRequest import islandServerRequest
from threading import Thread, RLock
import time
from robot.communication.ObtenirTension import ObtenirTension

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
        self.lettreObtenue = None
        self.indiceObtenu = None
        self.pretEnvoyerLettre = False
        self.pretEnvoyerIndice = False
        # self.demarrerAlignementIle()
        self.adresseIP = '10.248.184.232'
        # self.adresseIP = '132.203.14.228'
        self.demarrerLectureUART()
        # self.demarrerObtenirTension()
        self.demarrerConnectionTCP()
        # cible = self.effectuerRequeteServeur('X')
        # self.determinerCible(cible)
        # self.demarrerAlignementTresor()

    def run(self):
        print("Robot initialized")
        self.uartDriver.monterPrehenseur()
        self.uartDriver.cameraPositionDepot()
        time.sleep(1)
        self.uartDriver.cameraPositionFace()
        print("Prehenseur et camera position defaut")

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        print("Demarre TCP Client")
        self.robotClient = RobotClient(self, self.adresseIP)
        self.robotClient.start()

    def demarrerLectureUART(self):
        print "Demarrer lecture UART"
        self.threadLecture = LectureUART(self)
        self.threadLecture.start()

    def demarrerObtenirTension(self):
        print "Demarrer obtention tension."
        self.obtenirTension = ObtenirTension(self)
        self.obtenirTension.start()

    def demarrerAlignementIle(self):
        self.demarrerFeedVideo()
        self.alignementEnCours = True
        print("######### CAMERA DOWN #########")
        self.uartDriver.cameraPositionDepot()
        time.sleep(2)
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self, 'bleu')
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

        print("######### COMMENCE AUTO PILOT #########")
        self.executerAlignement()
        time.sleep(0.5)
        self.uartDriver.postAlignementIle()
        print("======== ALIGNEMENT TERMINER ========")
        self.alignementEnCours = False

    def demarrerAlignementTresor(self):
        self.demarrerFeedVideo()
        self.alignementEnCours = True
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self, 'tresor')
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()
        self.uartDriver.descendrePrehenseur()
        time.sleep(6)
        print("######### PREHENSEUR DOWN #########")
        while not (self.commandeTerminee):
            print("If this prints, this is useful")
            time.sleep(1)
        self.uartDriver.cameraPositionTresor()
        print("######### CAMERA DOWN #########")
        time.sleep(2)
        self.uartDriver.activerAimant()
        time.sleep(0.5)
        self.executerAlignement()
        self.uartDriver.sendCommand('forward', 20)
        time.sleep(4)
        print("######### COMMENCE AUTO PILOT #########")
        self.uartDriver.postAlignementTresor()
        print("======== ALIGNEMENT TERMINER ========")
        self.alignementEnCours = False

    def demarrerAlignementStation(self):
        self.demarrerFeedVideo()
        self.alignementEnCours = True
        # self.analyseImageEmbarquee = AnalyseImageEmbarquee(self, 'station')
        # self.analyseImageEmbarquee.start()
        # self.analyseImageEmbarquee.join()
        self.uartDriver.monterPrehenseur()
        time.sleep(5)
        print("######### PREHENSEUR UP #########")
        while not (self.commandeTerminee):
            print("If this prints, this is useful")
            time.sleep(1)
        self.uartDriver.cameraPositionFace()
        print("######### CAMERA FRONT #########")
        time.sleep(2)
        #self.executerAlignement()
        self.uartDriver.chargerCondensateur()
        time.sleep(1)
        print("######### CONDENSATEUR ON ##########")
        self.uartDriver.sendCommand('forward', 10)
        time.sleep(3)
        print("######### COMMENCE RECHARGE #########")
        print("TENSION AVANT RECHARGE: %s" %self.tensionCondensateur)

        while(float(self.tensionCondensateur) < 4.60):
             print(self.tensionCondensateur)
             print("Tension condensateur: %s" %self.tensionCondensateur)
             time.sleep(0.5)

        self.uartDriver.stopCondensateur()
        print("######### CONDENSATEUR OFF ##########")
        time.sleep(2)

        print("Envoie signal pour decoder le manchester")
        self.decoderManchester()

        self.uartDriver.postAlignementStation()
        print("======== ALIGNEMENT TERMINER ========")

        self.alignementEnCours = False

    def decoderManchester(self):
        self.uartDriver.decoderManchester()
        self.attendreReceptionLettre()
        reponse = self.effectuerRequeteServeur(self.lettreObtenue)
        self.determinerCible(reponse)

    def determinerCible(self, reponse):
        if "forme" in reponse:
            if "carre" in reponse:
                self.indiceObtenu = "carre"
            elif "pentagone" in reponse:
                self.indiceObtenu = "pentagone"
            elif "cercle" in reponse:
                self.indiceObtenu = "cercle"
            elif "triangle" in reponse:
                self.indiceObtenu = "triangle"
            else:
                print("FUCK")
            self.pretEnvoyerIndice = True

        elif "couleur" in reponse:
            if "rouge" in reponse:
                self.indiceObtenu = "rouge"
            elif "bleu" in reponse:
                self.indiceObtenu = "bleu"
            elif "vert" in reponse:
                self.indiceObtenu = "vert"
            elif "jaune" in reponse:
                self.indiceObtenu = "jaune"
            else:
                print("FUCK")
            self.pretEnvoyerIndice = True
        else:
            print("Something wrong")

    def attendreReceptionLettre(self):
        while (self.lettreObtenue is None):
            print("Waiting for Manchester...")
            time.sleep(2)
        print("Lettre recu par le robot : %s" % self.lettreObtenue)
        self.pretEnvoyerLettre = True

    def effectuerRequeteServeur(self, lettre):
        reponse = islandServerRequest(self.adresseIP, lettre)
        return reponse

    def executerAlignement(self):
        for inst in self.instructions:
            self.commandeTerminee = False
            commande, parametre = inst
            self.uartDriver.sendCommand(commande, parametre)
            print("Commande envoyee:", commande, parametre)
            time.sleep(5)
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
        elif (commande == 'alignement_tresor'):
            print("Commence phase alignement: %s" % parametre)
            self.demarrerAlignementTresor()
        elif (commande == 'alignement_station'):
            print("Commence phase alignement: %s" % parametre)
            self.demarrerAlignementStation()
        else:
            self.uartDriver.sendCommand(commande, parametre)
            print("Commande envoye au UART")
