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
    def __init__(self):
        Thread.__init__(self)
        self.trajectoireReel = None
        self.trajectoirePrevue = None
        self.angleDesire = None
        self.tensionCondensateur = 0
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
                self.demarerRoutine()
            time.sleep(0.1)

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
        self.etapeStation()
        self.etapeTresor()
        self.etapeIle()
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

    def etapeIle(self):
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
        self.allignement("allignementIle")
        print '\n--------------------------------------------------'
        print 'Depot termine.'
        print '--------------------------------------------------'

    def etapeTresor(self):
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
        self.allignement("allignementTresor")
        print '\n--------------------------------------------------'
        print 'Capture termine.'
        print '--------------------------------------------------'

    def etapeStation(self):
        print '\n--------------------------------------------------'
        print 'Aller a la station de recharge...'
        print '--------------------------------------------------'
        destination = self.identifierDestination('RECHARGE')
        self.trouverTrajectoirePrevu(destination)
        while len(self.trajectoireReel) > 1:
            self.orienter()
            self.deplacer()
        self.angleDesire = 90
        self.orienter()
        print '\n--------------------------------------------------'
        print 'Arriver a la station de recharge.'
        print '--------------------------------------------------'
        self.allignement("allignementStation")
        print '\n--------------------------------------------------'
        print 'Recharge termine.'
        print '--------------------------------------------------'

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
            except:
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
            time.sleep(0.03)

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
            if angle <= 2 and angle >= -2:
                print '\nOrientation termine.'
                break
            self.myRequest = RequeteJSON("rotate", angle)
            self.envoyerCommande = True
            self.attendreRobot()
            self.angleDesire = None

    def attendreRobot(self):
        print '\nAttente du robot...'
        self.attenteDuRobot = True
        while self.attenteDuRobot:
            time.sleep(0.1)
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
        if dep <= 25:
            print '\nArriver.'
            self.trajectoireReel.pop(-1)

    def allignement(self, type):
        self.myRequest = RequeteJSON(type, 0)
        self.envoyerCommande = True
        self.attendreRobot()




