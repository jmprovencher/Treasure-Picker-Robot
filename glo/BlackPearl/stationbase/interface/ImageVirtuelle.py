from threading import Thread
import time
import cv2
import copy

MIN_ANCIENNE_POSITION_ROBOT = 2
MIN_TRAJECTOIRE = 1
COULEUR_ROUGE = 'Rouge'
COULEUR_JAUNE = 'Jaune'
COULEUR_VERT = 'Vert'
COULEUR_BLEU = 'Bleu'

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
            self.chargerImageVirtuelle()
            if self.stationBase.getTrajectoirePrevue() is not None:
                self.dessinerTrajetPrevu()
            time.sleep(0.01)

    def chargerImageVirtuelle(self):
        self.imageVirtuelle = copy.deepcopy(self.stationBase.threadAnalyseImageWorld.imageCropper)
        self.dessinerElementCarto()

    def dessinerElementCarto(self):
        for ile in self.stationBase.getCarte().getIles():
            cv2.putText(self.imageVirtuelle, ile.getForme(), (ile.getX() - 25, ile.getY()),
                        self.police, 0.5, self.getColor(ile.getCouleur()), 1, cv2.LINE_AA)
        for tresor in self.stationBase.getCarte().getTresors():
            cv2.putText(self.imageVirtuelle, 'Tresor', (tresor.getX() - 25, tresor.getY()),
                        self.police, 0.5, self.getColor('Jaune'), 1, cv2.LINE_AA)

        self.dessinerRobot()

    def dessinerRobot(self):
        if self.stationBase.getCarte().getRobot() is not None:
            position = (self.stationBase.getCarte().getRobot().getX(), self.stationBase.getCarte().getRobot().getY())
            self.anciennePosRobot.append(position)
            if len(self.anciennePosRobot) >= MIN_ANCIENNE_POSITION_ROBOT:
                for i in reversed(range(len(self.anciennePosRobot)-1)):
                    cv2.arrowedLine(self.imageVirtuelle, self.anciennePosRobot[i],
                                    self.anciennePosRobot[i+1], (0, 0, 0), 2)
        else:
            self.anciennePosRobot = []

    def dessinerTrajetPrevu(self):
        if len(self.stationBase.getTrajectoirePrevue()) > MIN_TRAJECTOIRE:
            pointInitial = None
            for pointFinal in self.stationBase.getTrajectoirePrevue():
                if pointInitial is None:
                    pointInitial = pointFinal
                else:
                    cv2.arrowedLine(self.imageVirtuelle, pointFinal, pointInitial, (0, 255, 0), 2)
                    pointInitial = pointFinal
        else:
            cv2.putText(self.imageVirtuelle, 'Phase d''alignement', (1000, 800), self.police, 1,
                        (0, 0, 0), 1, cv2.LINE_AA)

    def getColor(self, couleur):
        if couleur == COULEUR_ROUGE:
            return 0, 0, 255
        elif couleur == COULEUR_JAUNE:
            return 0, 255, 255
        elif couleur == COULEUR_VERT:
            return 0, 255, 0
        elif couleur == COULEUR_BLEU:
            return 255, 0, 0
        return 0, 0, 0

