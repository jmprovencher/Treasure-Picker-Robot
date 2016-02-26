# import the necessary packages
import cv2
import Config
from elements.Ile import Ile
from elements.Tresor import Tresor
from stationbase.vision.DetectionElementsCartographiques import DetectionElementsCartographiques


##### REFACTORING STATUS #####
# Done

class AnalyseImageWorld(object):
    def __init__(self):
        self.elementsCartographiques = []
        self.tresorIdentifies = []
        self.resolution = (1200, 1600)
        self.police = cv2.FONT_HERSHEY_SIMPLEX

    def chargerImage(self, url):
        self.imageCamera = cv2.imread(Config.Config().appendToProjectPath(url))
        self.recadrerImage()
        self.estomperImage()

    def recadrerImage(self):
        crop = self.imageCamera[100:950, 0:1600]
        cv2.imwrite(Config.Config().appendToProjectPath('Cropped.png'), crop)
        self.imageCamera = cv2.imread(Config.Config().appendToProjectPath('Cropped.png'))

    def estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(Config.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(Config.Config().appendToProjectPath('Cropped.png'))

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])

        return centre_x, centre_y

    def identifierForme(self, forme):
        contoursForme, nomForme, couleurForme = forme
        centreForme = self.trouverCentreForme(contoursForme)

        if (couleurForme == ""):
            tresor = Tresor(centreForme)
            self.elementsCartographiques.append(tresor)
        else:
            ile = Ile(centreForme, couleurForme, nomForme)
            self.elementsCartographiques.append(ile)

    def trouverElementCartographiques(self):
        detectionIles = DetectionElementsCartographiques(self.imageCamera)
        detectionIles.detecterIles()
        detectionIles.detecterTresor()

        self.ilesIdentifiees = detectionIles.ilesIdentifiees
        self.tresorIdentifies = detectionIles.tresorIdentifies

        for element in self.ilesIdentifiees:
            self.identifierForme(element)
        for tresor in self.tresorIdentifies:
            self.identifierForme(tresor)

    def dessinerTrajet(self, trajet):
        pointInitial = None

        if (len(trajet) == 0):
            cv2.putText(self.imageCamera, 'Aucun trajet disponible', (1000, 800), self.police, 1.5,
                        (0, 0, 255), 2, cv2.LINE_AA)
        else:
            for pointFinal in trajet:
                if (pointInitial == None):
                    pointInitial = pointFinal
                else:
                    cv2.arrowedLine(self.imageCamera, pointFinal, pointInitial, (0, 255, 0), 5)
                    pointInitial = pointFinal

    def dessinerElementCartographique(self):
        for element in self.elementsCartographiques:
            cv2.putText(self.imageCamera, element.forme, (element.centre_x - 25, element.centre_y),
                        self.police, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def dessinerDebutFinTrajet(self, pointInitial, pointFinal):
        debut_x, debut_y = pointInitial
        fin_x, fin_y = pointFinal

        cv2.putText(self.imageCamera, 'Debut', (debut_x - 25, debut_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.imageCamera, 'Fin', (fin_x, fin_y), self.police, 1, (0, 0, 0), 2, cv2.LINE_AA)

    def afficherImage(self):
        cv2.imshow('Image', self.imageCamera)
        cv2.waitKey(0)
