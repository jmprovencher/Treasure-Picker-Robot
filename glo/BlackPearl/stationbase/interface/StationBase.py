# import the necessary packages
from __future__ import division
from elements.Carte import Carte
from stationbase.vision.AnalyseImageWorld import AnalyseImageWorld
from stationbase.interface.FeedVideoStation import FeedVideoStation
from stationbase.communication.StationServeur import StationServeur
from stationbase.interface.ImageVirtuelle import ImageVirtuelle
from threading import Thread, RLock
import time
import math
from stationbase.communication.RequeteJSON import RequeteJSON
import copy

verrou = RLock()

class StationBase(Thread):
    def __init__(self, etape):
        Thread.__init__(self)
        self.etape = etape
        self.trajectoireReel = None
        self.trajectoirePrevue = None
        self.angleDesire = None
        self.tensionCondensateur = 0
        self.descriptionIleCible = "?"
        self.manchester = "?"
        self.arriver = False
        self.envoyerCommande = False
        self.robotEstPret = False
        self.attenteDuRobot = False
        self.demarrerConnectionTCP()
        self.demarrerFeedVideo()
        self.carte = Carte()
        self.demarrerAnalyseImageWorld()
        self.initialisationTrajectoire()
        self.demarrerImageVirtuelle()

    def run(self):
        print '\nAttendre que le robot soit pret...'
        while 1:
            if self.robotEstPret == True:
                print 'Robot est pret'
                break
            time.sleep(0.01)
        self.choisirEtape(self.etape)
        time.sleep(0.01)

    def choisirEtape(self, etape):
        if (etape == 'routine complete'):
            self.demarerRoutine()
        elif (etape == 'deplacement station'):
            self.deplacementStation()
        elif (etape == 'alignement station'):
            self.alignerStation()
        elif (etape == 'deplacement tresor'):
            self.deplacementTresor()
        elif (etape == 'alignement tresor'):
            self.alignerTresor()
        elif (etape == 'deplacement ile'):
            self.deplacementIle()
        elif (etape == 'alignement ile'):
            self.alignerIle()

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

    def demarerRoutine(self):
        self.deplacementStation()
        self.alignerStation()
        self.deplacementTresor()
        self.alignerTresor()
        self.deplacementIle()
        self.alignerIle()
        time.sleep(100000)

    def initialisationTrajectoire(self):
        self.carte.trajectoire.initGrilleCellule(self.carte.listeIles)

    def identifierDestination(self, etape):
        print '\nIndentifier destination'
        destination = None
        if (etape == 'RECHARGE'):
            destination = self.carte.stationRecharge.getCentre()
        elif (etape == 'TRESOR'):
            destination = self.carte.cible.tresorChoisi.getCentre()
        elif (etape == 'ILE'):
            destination = self.carte.cible.ileChoisie.getCentre()
        if destination is None:
            print 'erreur! Aucune destination trouvee.'
        return destination

    def deplacementIle(self):
        print '\n--------------------------------------------------'
        print 'Aller a l''ile cible...'
        print '--------------------------------------------------'
        destination = self.identifierDestination('ILE')
        self.trouverTrajectoirePrevu(destination)
        while len(self.trajectoireReel) > 1:
            self.orienter()
            self.deplacer()
        print '\n--------------------------------------------------'
        print 'Arriver a l''ile.'
        print '--------------------------------------------------'

    def alignerIle(self):
        self.allignement("alignement_ile", 0)
        print '\n--------------------------------------------------'
        print 'Depot termine.'
        print '--------------------------------------------------'

    def deplacementTresor(self):
        print '\n--------------------------------------------------'
        print 'Aller au tresor...'
        print '--------------------------------------------------'
        destination = self.identifierDestination('TRESOR')
        self.trouverTrajectoirePrevu(destination)
        while len(self.trajectoireReel) > 1:
            self.orienter()
            self.deplacer()
        if self.carte.cible.tresorChoisi.getCentre()[1] < 100:
            self.angleDesire = 90
        elif self.carte.cible.tresorChoisi.getCentre()[1] > 750:
            self.angleDesire = 270
        self.orienter()
        print '\n--------------------------------------------------'
        print 'Arriver au tresor.'
        print '--------------------------------------------------'

    def alignerTresor(self):
        self.allignement("alignement_tresor", 0)
        print '\n--------------------------------------------------'
        print 'Capture termine.'
        print '--------------------------------------------------'

    def deplacementStation(self):
        print '\n--------------------------------------------------'
        print 'Aller a la station de recharge...'
        print '--------------------------------------------------'
        destination = self.identifierDestination('RECHARGE')
        self.trouverTrajectoirePrevu(destination)
        while (not self.trajectoireReel is None) or (len(self.trajectoireReel) > 1):
            self.orienter()
            self.deplacer()
            self.angleDesire = None
        self.angleDesire = 90
        self.orientationFinaleStation()
        self.reculer(5)
        print '\n--------------------------------------------------'
        print 'Arriver a la station de recharge.'
        print '--------------------------------------------------'

    def alignerStation(self):
        self.allignement("allignement_station", 0)
        print '\n--------------------------------------------------'
        print 'Recharge termine.'
        print '--------------------------------------------------'

    def reculer(self, dep):
        print '\nDeplacer'
        print 'deplacement: ', dep
        self.myRequest = RequeteJSON("backward", dep)
        self.envoyerCommande = True
        self.attendreRobot()

    def trouverTrajectoirePrevu(self, destination):
        print '\nTrouve la trajectoire prevu...'
        while 1:
            try:
                if (not self.carte.infoRobot is None):
                    self.trajectoirePrevue = self.carte.trajectoire.trouverTrajet(self.getPositionRobot(), destination)
                    if self.trajectoirePrevue is None:
                        print 'erreur! Aucun trajet trouve.'
                    else:
                        print 'trajet trouve.'
                    self.trajectoireReel = copy.deepcopy(self.trajectoirePrevue)
                    break
                time.sleep(0.01)
            except Exception as e:
                print e
                time.sleep(0.01)

    def trouverDeplacementOrientation(self):
        if self.angleDesire is None:
            arriver = self.trajectoireReel[-2]
            debut = self.getPositionRobot()
            self.angleDesire = self.trouverOrientationDesire(debut, arriver)
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

    def getPositionRobot(self):
        while 1:
            if (not self.carte.infoRobot is None):
                return copy.deepcopy(self.carte.infoRobot.getCentre())
            print 'robot introuvable'
            time.sleep(0.01)

    def getOrientationRobot(self):
        while 1:
            if (not self.carte.infoRobot is None):
                return self.carte.infoRobot.orientation
            time.sleep(0.01)


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

    def orienter(self):
        print '\nOrienter'
        while 1:
            angle = self.trouverDeplacementOrientation()
            if angle <= 5 and angle >= -5:
                print '\nOrientation termine.'
                break
            if angle >= 0:
                self.myRequest = RequeteJSON("rotateClockwise", angle)
            else:
                self.myRequest = RequeteJSON("rotateAntiClockwise", abs(angle))
            print 'Signaler que la comande est prete a envoyer.'
            self.envoyerCommande = True
            self.attendreRobot()
            self.angleDesire = None


    def orientationFinaleStation(self):
        print '\nOrienter'
        while 1:
            angle = self.trouverDeplacementOrientation()
            if angle <= 5 and angle >= -5:
                print '\nOrientation termine.'
                break
            if angle >= 0:
                self.myRequest = RequeteJSON("rotateClockwise", angle)
            else:
                self.myRequest = RequeteJSON("rotateAntiClockwise", abs(angle))
            print 'Signaler que la comande est prete a envoyer.'
            self.envoyerCommande = True
            self.attendreRobot()

    def attendreRobot(self):
        self.attenteDuRobot = True
        while self.attenteDuRobot:
            time.sleep(0.01)
        print 'Robot a fini.'

    def distanceADestinationAuCarre(self, x, y, destX, destY):
        distanceX = destX - x
        distanceY = destY - y
        distanceX = self.carte.trajectoire.grilleCellule.depPixelXACentimetre(distanceX)
        distanceY = self.carte.trajectoire.grilleCellule.depPixelYACentimetre(distanceY)
        distanceCarre = distanceX**2 + distanceY**2
        return distanceCarre

    def distanceADestination(self, x, y, destX, destY):
        distancePixX = destX - x
        distancePixY = destY - y
        distanceX = self.carte.trajectoire.grilleCellule.depPixelXACentimetre(distancePixX)
        distanceY = self.carte.trajectoire.grilleCellule.depPixelYACentimetre(distancePixY)
        distance = int(round(math.sqrt(distanceX**2 + distanceY**2)))
        return distance

    def deplacer(self):
        print '\nDeplacer'
        arriver = self.trajectoireReel[-2]
        debut = self.getPositionRobot()
        dep = self.distanceADestination(debut[0], debut[1], arriver[0], arriver[1])
        print 'deplacement: ', dep
        self.myRequest = RequeteJSON("forward", dep)
        self.envoyerCommande = True
        self.attendreRobot()
        debut = self.getPositionRobot()
        dep = self.distanceADestinationAuCarre(debut[0], debut[1], arriver[0], arriver[1])
        if dep <= 64:
            print '\nArriver.'
            if len(self.trajectoireReel) == 2:
                self.trajectoireReel = None
            else:
                self.trajectoireReel.pop(-1)

    def allignement(self, commande, parametre):
        self.myRequest = RequeteJSON(commande, parametre)
        self.envoyerCommande = True
        self.attendreRobot()
        




