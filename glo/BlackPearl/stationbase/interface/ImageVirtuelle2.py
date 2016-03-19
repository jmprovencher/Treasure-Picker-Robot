import sys
from threading import Thread, RLock
import ConfigPath
import time
import cv2

verrou = RLock()

class ImageVirtuelle2(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.chargerImageVirtuelle()
        self.police = cv2.FONT_HERSHEY_SIMPLEX
        self.dessinerElementCarto()

    def run(self):
        while 1:
            cv2.imshow('Image Virtuelle', self.imageVirtuelle)
            time.sleep(1)

    def chargerImageVirtuelle(self):
        self.imageVirtuelle = self.imageVirtuelle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/imageVide.png'))
        self.recadrerImage()

    def dessinerElementCarto(self):
        for ile in self.stationBase.carte.listeIles:
            cv2.putText(self.imageVirtuelle, ile.forme, (ile.centre_x - 25, ile.centre_y),
                        self.police, 0.5, self.getColor(ile.couleur), 1, cv2.LINE_AA)
        for tresor in self.stationBase.carte.listeTresors:
            cv2.putText(self.imageVirtuelle, tresor.forme, (tresor.centre_x - 25, ile.centre_y),
                        self.police, 0.5, self.getColor('Jaune'), 1, cv2.LINE_AA)

    def recadrerImage(self):
        self.imageVirtuelle = self.imageVirtuelle[155:1010, 0:1600]

    def dessinerTrajetPrevu(self, debut, fin, trajet):
        self.dessinerDebutFinTrajetPrevu(debut, fin)
        pointInitial = None
        if (len(trajet) == 0):
            cv2.putText(self.imageVirtuelle, 'Aucun trajet disponible', (1000, 800), self.police, 1.5,
                        (0, 0, 255), 2, cv2.LINE_AA)
        else:
            for pointFinal in trajet:
                if (pointInitial == None):
                    pointInitial = pointFinal
                else:
                    cv2.arrowedLine(self.imageVirtuelle, pointFinal, pointInitial, (0, 255, 0), 5)
                    pointInitial = pointFinal

    def dessinerDebutFinTrajetPrevu(self, debut, fin):
        debut_x, debut_y = debut
        fin_x, fin_y = fin
        cv2.putText(self.imageVirtuelle, 'Debut', (debut_x - 25, debut_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.imageVirtuelle, 'Fin', (fin_x, fin_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)

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

