import sys
from threading import Thread, RLock
import ConfigPath
import time
import cv2

verrou = RLock()

class ImageVirtuelle(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.imageVirtuelle = None
        self.anciennePosRobot = []
        self.police = cv2.FONT_HERSHEY_SIMPLEX
        self.chargerImageVirtuelle()

    def run(self):
        while 1:
            if (not self.stationBase.trajectoirePrevue is None):
                self.dessinerTrajetPrevu()
            self.chargerImageVirtuelle()
            time.sleep(0.01)

    def chargerImageVirtuelle(self):
        self.imageVirtuelle = self.stationBase.threadAnalyseImageWorld.imageCropper
        self.dessinerElementCarto()

    def dessinerElementCarto(self):
        for ile in self.stationBase.carte.listeIles:
            cv2.putText(self.imageVirtuelle, ile.forme, (ile.centre_x - 25, ile.centre_y),
                        self.police, 0.5, self.getColor(ile.couleur), 1, cv2.LINE_AA)
        for tresor in self.stationBase.carte.listeTresors:
            cv2.putText(self.imageVirtuelle, tresor.forme, (tresor.centre_x - 25, tresor.centre_y),
                        self.police, 0.5, self.getColor('Jaune'), 1, cv2.LINE_AA)
        self.dessinerRobot()

    def dessinerTrajetPrevu(self):
        if (len(self.stationBase.trajectoirePrevue) > 1):
            self.dessinerDebutFinTrajetPrevu(self.stationBase.trajectoirePrevue[-1], self.stationBase.trajectoirePrevue[0])
            pointInitial = None
            for pointFinal in self.stationBase.trajectoirePrevue:
                if (pointInitial == None):
                    pointInitial = pointFinal
                else:
                    cv2.arrowedLine(self.imageVirtuelle, pointFinal, pointInitial, (0, 255, 0), 2)
                    pointInitial = pointFinal
        else:
            cv2.putText(self.imageVirtuelle, 'Aucun trajet disponible', (1000, 800), self.police, 1.5,
                    (0, 0, 255), 1, cv2.LINE_AA)

    def dessinerDebutFinTrajetPrevu(self, debut, fin):
        debut_x, debut_y = debut
        fin_x, fin_y = fin
        cv2.putText(self.imageVirtuelle, 'Debut', (debut_x - 25, debut_y), self.police, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(self.imageVirtuelle, 'Fin', (fin_x, fin_y), self.police, 1, (0, 0, 0), 1, cv2.LINE_AA)

    def dessinerRobot(self):
        if (not self.stationBase.carte.infoRobot is None):
            position = (self.stationBase.carte.infoRobot.centre_x, self.stationBase.carte.infoRobot.centre_y)
            self.anciennePosRobot.append(position)
            if (len(self.anciennePosRobot) >= 2):
                for i in reversed(range(len(self.anciennePosRobot)-1)):
                    cv2.arrowedLine(self.imageVirtuelle, self.anciennePosRobot[i], self.anciennePosRobot[i+1], (0,0,0), 2)
        else:
            self.anciennePosRobot = []

    def getColor(self, couleur):
        if (couleur == 'Rouge'):
            return (0,0,255)
        elif (couleur == 'Jaune'):
            return (0,255,255)
        elif (couleur == 'Vert'):
            return (0,255,0)
        elif (couleur == 'Bleu'):
            return (255,0,0)
        return (0,0,0)

