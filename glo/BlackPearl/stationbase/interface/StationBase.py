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
        self.rapport = 1.16
        self.coordonneeXMilieu = 813
        self.coordonneeYMilieu = 410
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
        if etape == 'routine complete':
            self.demarerRoutine()
            self.roundTerminee = True
        elif etape == 'deplacement station':
            self.deplacement('RECHARGE')
        elif etape == 'alignement station':
            self.aligner("alignement_station")
            self.trouverTresorEtCible()
            self.attendreRobot()
        elif etape == 'deplacement tresor':
            self.trouverTresorEtCible()
            self.attendreRobot()
            self.attendreThreadCible()
            self.deplacement('TRESOR')
            RequeteJSON("cameraTreasure", 0)
            self.threadCommunication.signalerEnvoyerCommande()
        elif etape == 'alignement tresor':
            self.aligner("alignement_tresor")
        elif etape == 'deplacement ile':
            self.carte.getCible().trouverIleCible()
            self.deplacement('ILE')
        elif etape == 'alignement ile':
            self.aligner("alignement_ile")
        elif etape == 'decoder manchester':
            self.decoderManchester()

    def demarerRoutine(self):
        self.deplacement('RECHARGE')
        self.aligner("alignement_station")
        self.trouverTresorEtCible()
        self.attendreRobot()
        self.attendreThreadCible()
        while not self.threadCommunication.tresorTrouve:
            self.deplacement('TRESOR')
            self.aligner("alignement_tresor")
            time.sleep(0.01)
        self.deplacement('ILE')
        self.aligner("alignement_ile")
        self.roundTerminee = True

    def deplacement(self, type):
        print '\n--------------------------------------------------'
        print 'Etape de deplacement : %s' % type
        print '--------------------------------------------------'
        destination = self.identifierDestination(type)
        self.trouverTrajectoirePrevu(destination, type)
        while (self.trajectoireReel is not None) and (len(self.trajectoireReel) > 1):
            self.orienter('deplacement')
            self.deplacer()
        self.correctionsFinales(type)
        print '\n--------------------------------------------------'
        print 'Arriver.'
        print '--------------------------------------------------'

    def identifierDestination(self, etape):
        print '\nIndentifier destination'
        destination = None
        if etape == 'RECHARGE':
            destination = self.carte.getStationRecharge().getCentre()
        elif etape == 'TRESOR':
            destination = self.carte.cible.possibilite[self.carte.cible.conteur].getCentre()
            print 'identifier destination tresor'
            print destination
        elif etape == 'ILE':
            destination = self.carte.cible.ileChoisie.getCentre()
        if destination is None:
            print 'erreur! Aucune destination trouvee.'
        return destination

    def correctionsFinales(self, type):
        if type == 'RECHARGE':
            self.angleDesire = 88
            self.orienter(type)
            self.deplacementArriere(5)
            self.deplacementDroit(13)
        elif type == 'TRESOR':
            if self.carte.getCible().getTresorCible().getCentre()[1] < 500:
                self.angleDesire = 90
                self.carte.cible.conteur += 1
            else:
                self.angleDesire = 270
                self.carte.cible.conteur += 1
            self.orienter(type)
            self.deplacementArriere(3)
        elif type == 'ILE':
            arriver = self.carte.getCible().getIleCible().getCentre()
            debut = self.getPositionRobot()
            #debut = self.correctionCentre(debut)
            self.angleDesire = self.trouverOrientationDesire(debut, arriver)
            self.orienter(type)
        self.trajectoirePrevue = None

    def aligner(self, type):
        print '\n--------------------------------------------------'
        print 'Debuter l''alignement.'
        print '--------------------------------------------------'
        int = 0
        if type == 'alignement_ile':
            couleur = self.carte.getCible().getIleCible().getCouleur()
            #couleur = 'Bleu'
            if couleur == 'Vert':
                int = 0
            elif couleur == 'Bleu':
                int = 1
            elif couleur == 'Jaune':
                int = 2
            elif couleur == 'Rouge':
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
        self.trajectoirePrevue = self.carte.trajectoire.trouverTrajet(self.getPositionRobot(), destination, type)
        if self.trajectoirePrevue is None:
            print 'erreur! Aucun trajet trouve.'
        else:
            print 'trajet trouve.'
        self.trajectoireReel = copy.deepcopy(self.trajectoirePrevue)

    def orienter(self, type):
        print '\nOrienter'
        conteur = 0
        while 1:
            reduction = 0
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
        centre = copy.deepcopy(self.carte.getRobotValide().getCentre())
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




