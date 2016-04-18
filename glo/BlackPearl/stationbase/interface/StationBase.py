from __future__ import division
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideoStation import FeedVideoStation
from stationbase.communication.StationServeur import StationServeur
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
from threading import Thread
import time
import math
from stationbase.communication.RequeteJSON import RequeteJSON
import copy
from timeit import default_timer
from stationbase.vision.TrouverTresorEtCible import TrouverTresorEtCible
from elements.Cible import Cible

ETAPE_ROUTINE_COMPLETE = 'routine complete'
ETAPE_DEPLACEMENT_STATION = 'deplacement station'
ETAPE_ALIGNEMENT_STATION = 'alignement station'
ETAPE_DEPLACEMENT_TRESOR = 'deplacement tresor'
ETAPE_ALIGNEMENT_TRESOR = 'alignement tresor'
ETAPE_DEPLACEMENT_ILE = 'deplacement ile'
ETAPE_ALIGNEMENT_ILE = 'alignement ile'
ETAPE_MANCHESTER = 'decoder manchester'
ETAPE_RECHARGE = 'RECHARGE'
ETAPE_TRESOR = 'TRESOR'
ETAPE_ILE = 'ILE'
COULEUR_VERT = 'Vert'
COULEUR_BLEU = 'Bleu'
COULEUR_JAUNE = 'Jaune'
COULEUR_ROUGE = 'Rouge'
MAX_CENTRE_TRESOR = 500
MIN_TRAJECTOIRE = 1


class StationBase(Thread):
    def __init__(self, etape, numeroTable):
        Thread.__init__(self)
        self.startTimer = default_timer()
        self.numeroTable = numeroTable
        self.etape = etape
        self.trajectoireReel = None
        self.trajectoirePrevue = None
        self.angleDesire = None
        self.tensionCondensateur = "0"
        self.descriptionIleCible = "?"
        self.manchester = "?"
        self.roundTerminee = False
        self.rapport = 0.84
        self.coordonneeXMilieu = 787
        self.coordonneeYMilieu = 419
        self.carte = Carte()
        self.demarrerConnectionTCP()
        self.demarrerFeedVideo()
        self.demarrerAnalyseImageWorld()
        self.demarrerImageVirtuelle()

    def run(self):
        self.attendreFinDeDetectionPrimaire()
        self.initialisationTrajectoire()
        self.attendreRobotPret()
        self.choisirEtape(self.etape)
        time.sleep(10)

    def choisirEtape(self, etape):
        if etape == ETAPE_ROUTINE_COMPLETE:
            self.demarerRoutine()
            self.roundTerminee = True
        elif etape == ETAPE_DEPLACEMENT_STATION:
            self.deplacement(ETAPE_RECHARGE)
        elif etape == ETAPE_ALIGNEMENT_STATION:
            self.aligner(ETAPE_ALIGNEMENT_STATION)
            self.trouverTresorEtCible()
            self.attendreRobot()
        elif etape == ETAPE_DEPLACEMENT_TRESOR:
            self.trouverTresorEtCible()
            self.attendreRobot()
            self.attendreThreadCible()
            self.deplacement(ETAPE_TRESOR)
            RequeteJSON("cameraTreasure", 0)
            self.threadCommunication.signalerEnvoyerCommande()
        elif etape == ETAPE_ALIGNEMENT_TRESOR:
            self.aligner(ETAPE_ALIGNEMENT_TRESOR)
        elif etape == ETAPE_DEPLACEMENT_ILE:
            self.carte.cible = Cible([self.carte])
            self.deplacement(ETAPE_ILE)
        elif etape == ETAPE_ALIGNEMENT_ILE:
            self.carte.cible = Cible([self.carte])
            self.aligner(ETAPE_ALIGNEMENT_ILE)
        elif etape == ETAPE_MANCHESTER:
            self.decoderManchester()

    def demarerRoutine(self):
        self.deplacement(ETAPE_RECHARGE)
        self.aligner(ETAPE_ALIGNEMENT_STATION)
        self.trouverTresorEtCible()
        self.attendreRobot()
        self.attendreThreadCible()
        while not self.threadCommunication.tresorTrouve:
            self.deplacement(ETAPE_TRESOR)
            self.aligner(ETAPE_ALIGNEMENT_TRESOR)
            time.sleep(0.01)
        self.deplacement(ETAPE_ILE)
        self.aligner(ETAPE_ALIGNEMENT_ILE)
        self.roundTerminee = True

    def deplacement(self, type):
        print '\n--------------------------------------------------'
        print 'Etape de deplacement : %s' % type
        print '--------------------------------------------------'
        destination = self.identifierDestination(type)
        self.trouverTrajectoirePrevu(destination, type)
        while (self.trajectoireReel is not None) and (len(self.trajectoireReel) > MIN_TRAJECTOIRE):
            self.orienter('deplacement')
            self.deplacer()
        self.correctionsFinales(type)
        print '\n--------------------------------------------------'
        print 'Arriver.'
        print '--------------------------------------------------'

    def identifierDestination(self, etape):
        print '\nIndentifier destination'
        destination = None
        if etape == ETAPE_RECHARGE:
            destination = self.carte.getStationRecharge().getCentre()
        elif etape == ETAPE_TRESOR:
            destination = self.carte.cible.tresorChoisi.getCentre()
            print 'identifier destination tresor'
            print destination
        elif etape == ETAPE_ILE:
            destination = self.carte.cible.ileChoisie.getCentre()
        if destination is None:
            print 'erreur! Aucune destination trouvee.'
        return destination

    def correctionsFinales(self, type):
        if type == ETAPE_RECHARGE:
            self.angleDesire = 90
            self.orienter(type)
            self.deplacementArriere(5)
            self.deplacementDroit(10)
        elif type == ETAPE_TRESOR:
            if self.carte.getCible().getTresorCible().getCentre()[1] < MAX_CENTRE_TRESOR:
                self.angleDesire = 90
                self.carte.cible.conteur += 1
            else:
                self.angleDesire = 270
                self.carte.cible.conteur += 1
            self.orienter(type)
            self.deplacementArriere(7)
        elif type == ETAPE_ILE:
            arriver = self.carte.getCible().getIleCible().getCentre()
            debut = self.getPositionRobot()
            print 'arrive: ', arriver
            print 'robot: ', debut
            debut2 = self.correctionCentre(debut)
            print 'robot2: ', debut2
            self.angleDesire = self.trouverOrientationDesire(debut2, arriver)
            print self.angleDesire
            self.orienter(type)
        self.trajectoirePrevue = None

    def aligner(self, type):
        print '\n--------------------------------------------------'
        print 'Debuter l''alignement.'
        print '--------------------------------------------------'
        int = 0
        if type == 'alignement_ile':
            couleur = self.carte.getCible().getIleCible().getCouleur()
            if couleur == COULEUR_VERT:
                int = 0
            elif couleur == COULEUR_BLEU:
                int = 1
            elif couleur == COULEUR_JAUNE:
                int = 2
            elif couleur == COULEUR_ROUGE:
                int = 3
        RequeteJSON(type, int)
        self.threadCommunication.signalerEnvoyerCommande()
        if not type == 'alignement_station':
            self.attendreRobot()
        print '\n--------------------------------------------------'
        print 'Allignement termine.'
        print '--------------------------------------------------'

    def trouverTrajectoirePrevu(self, destination, type):
        print '\nTrouve la trajectoire prevu...'
        self.trajectoirePrevue = self.carte.trajectoire.trouverTrajet(self.getPositionRobot(), copy.deepcopy(destination), type)
        if self.trajectoirePrevue is None:
            print 'erreur! Aucun trajet trouve.'
        else:
            print 'trajet trouve.'
        self.trajectoireReel = copy.deepcopy(self.trajectoirePrevue)

    def orienter(self, type):
        print '\nOrienter'
        conteur = 0
        while 1:
            if self.angleDesire is None:
                arriver = self.trajectoireReel[-2]
                debut = self.getPositionRobot()
                self.angleDesire = self.trouverOrientationDesire(debut, arriver)
            angle = self.trouverDeplacementOrientation()
            if -3 <= angle <= 3:
                print '\nOrientation termine.'
                break
            if conteur >= 2:
                if angle > 0:
                    angle = 1
                else:
                    angle = -1
            if angle >= 0:
                RequeteJSON("rotateClockwise", angle)
            else:
                RequeteJSON("rotateAntiClockwise", abs(angle))
            print 'Signaler que la comande est prete a envoyer.'
            self.threadCommunication.signalerEnvoyerCommande()
            time.sleep(0.5)
            self.attendreRobot()
            if type == 'deplacement':
                self.angleDesire = None
            conteur += 1
        self.angleDesire = None

    def trouverOrientationDesire(self, debut, arriver):
        deltaX = arriver[0]-debut[0]
        deltaY = -1*(arriver[1]-debut[1])
        if not deltaX == 0:
            pente = deltaY/deltaX

        if deltaY == 0 and deltaX < 0:
            angle = 180
        elif deltaY == 0 and deltaX > 0:
            angle = 0
        elif deltaX == 0 and deltaY > 0:
            angle = 90
        elif deltaX == 0 and deltaY < 0:
            angle = 270
        elif deltaX > 0 and deltaY > 0:
            angle = int(round(math.degrees(math.atan(pente))))
        elif deltaX > 0 and deltaY < 0:
            angle = 360 + int(round(math.degrees(math.atan(pente))))
        elif deltaX < 0:
            angle = 180 + int(round(math.degrees(math.atan(pente))))

        return angle

    def trouverDeplacementOrientation(self):
        angleRobot = self.getOrientationRobot()
        print 'angle du robot: ', angleRobot
        print 'angle desire: ', self.angleDesire
        depDegre = angleRobot - self.angleDesire
        if depDegre < -180:
            depDegre = depDegre + 360
        elif depDegre > 180:
            depDegre = depDegre - 360
        print 'correction: ', depDegre

        return depDegre

    def deplacer(self):
        print '\nDeplacer'
        arriver = self.trajectoireReel[-2]
        debut = self.getPositionRobot()
        dep = self.distanceADestination(debut[0], debut[1], arriver[0], arriver[1])
        dep = int(round(dep))
        print 'deplacement: ', dep
        RequeteJSON("forward", dep)
        self.threadCommunication.signalerEnvoyerCommande()
        self.attendreRobot()
        debut = self.getPositionRobot()
        dep = self.distanceAuCarre(debut[0], debut[1], arriver[0], arriver[1])
        print '\nArriver.'
        if len(self.trajectoireReel) == 2:
            self.trajectoireReel = None
        else:
            self.trajectoireReel.pop(-1)

    def deplacementDroit(self, dep):
        print '\nDeplacer'
        print 'deplacement: ', dep
        RequeteJSON("right", dep)
        self.threadCommunication.signalerEnvoyerCommande()
        self.attendreRobot()

    def deplacementArriere(self, dep):
        print '\nDeplacer'
        print 'deplacement: ', dep
        RequeteJSON("backward", dep)
        self.threadCommunication.signalerEnvoyerCommande()
        self.attendreRobot()

    def deplacementAvant(self, dep):
        print '\nDeplacer'
        print 'deplacement: ', dep
        RequeteJSON("forward", dep)
        self.threadCommunication.signalerEnvoyerCommande()
        self.attendreRobot()

    def decoderManchester(self):
        RequeteJSON("decoderManchester", 0)
        self.threadCommunication.signalerEnvoyerCommande()
        self.attendreRobot()

    def demarrerFeedVideo(self):
        self.threadVideo = FeedVideoStation()
        self.threadVideo.start()

    def demarrerConnectionTCP(self):
        self.threadCommunication = StationServeur(self)
        self.threadCommunication.start()

    def demarrerAnalyseImageWorld(self):
        self.threadAnalyseImageWorld = AnalyseImageWorld(self)
        self.threadAnalyseImageWorld.start()

    def demarrerImageVirtuelle(self):
        self.threadImageVirtuelle = ImageVirtuelle(self)
        self.threadImageVirtuelle.start()

    def initialisationTrajectoire(self):
        self.carte.getTrajectoire().initGrilleCellule(self.carte.getIles())

    def trouverTresorEtCible(self):
        self.threadCible = TrouverTresorEtCible(self)
        self.threadCible.start()

    def attendreThreadCible(self):
        while self.threadCible.isAlive():
            time.sleep(0.01)
        print 'Cible trouve'

    def attendreRobotPret(self):
        print '\nAttendre que le robot soit pret...'
        while 1:
            if self.threadCommunication.getRobotPret():
                print 'Robot est pret'
                break
            time.sleep(0.01)

    def attendreRobot(self):
        self.threadCommunication.debuteAttenteDuRobot()
        while self.threadCommunication.getAttenteDuRobot():
            time.sleep(0.01)
        time.sleep(0.1)
        print 'Robot a fini.'

    def attendreCible(self):
        while self.carte.getCible() is None:
            time.sleep(0.01)

    def attendreFinDeDetectionPrimaire(self):
        while not self.threadAnalyseImageWorld.detectionPrimaireFini:
            time.sleep(0.01)

    def attendreFeed(self):
        while self.threadVideo.captureTable is None:
            time.sleep(0.01)

    def attendreImageVirtuelle(self):
        while self.threadImageVirtuelle.imageVirtuelle is None:
            time.sleep(0.01)

    def distanceAuCarre(self, x, y, x2, y2):
        return self.carte.getTrajectoire().distanceAuCarre(x, y, x2, y2)

    def distanceADestination(self, x, y, x2, y2):
        return math.sqrt(self.distanceAuCarre(x, y, x2, y2))

    def getImage(self):
        return copy.deepcopy(self.threadVideo.captureTable)

    def setRobot(self, robot):
        self.carte.robot = robot

    def getCarte(self):
        return self.carte

    def getManchester(self):
        return self.manchester

    def setManchester(self, lettre):
        self.manchester = lettre

    def getTensionCondensateur(self):
        return self.tensionCondensateur

    def setTensionCondensateur(self, tension):
        self.tensionCondensateur = tension

    def getTrajectoirePrevue(self):
        return self.trajectoirePrevue

    def getPositionRobot(self):
        centre = self.carte.getRobotValide().getCentre()
        return centre

    def getOrientationRobot(self):
        return self.carte.getRobotValide().orientation

    def getNumTable(self):
        return self.numeroTable

    def correctionCentre(self, centre):
        xNonCorrige = centre[0]
        deltaX = xNonCorrige - self.coordonneeXMilieu
        xCorriger = int(round(self.coordonneeXMilieu + (deltaX * self.rapport)))
        yNonCorrige = centre[1]
        deltaY = yNonCorrige - self.coordonneeYMilieu
        yCorriger = int(round(self.coordonneeYMilieu + (deltaY * self.rapport)))

        return xCorriger, yCorriger




