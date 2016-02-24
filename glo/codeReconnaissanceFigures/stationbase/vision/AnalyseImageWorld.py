# import the necessary packages
import cv2

from elements.Tresor import Tresor
from stationbase.vision.DetectionElementsCartographiques import DetectionElementsCartographiques
from elements.Ile import Ile


class AnalyseImageWorld(object):
    def __init__(self, url):
        self.elementsCartographiques = []
        self.tresorIdentifies = []
        self.chargerImage(url)
        self.resolution = (1200, 1600)
        self.recadrerImage()
        self.estomperImage()

    def chargerImage(self, url):
        self.imageCamera = cv2.imread(url)

    def recadrerImage(self):
        # Hardcodage du crop
        # TODO: a verifier sur toute les tables
        crop = self.imageCamera[100:950, 0:1600]

        cv2.imwrite('Cropped.png', crop)
        self.imageCamera = cv2.imread('Cropped.png')

    def estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite('Cropped.png', blur)
        self.imageCamera = cv2.imread('Cropped.png')

    def trouverCentreForme(self, contoursForme):
        MatriceCentreMasse = cv2.moments(contoursForme)
        centre_x = int(MatriceCentreMasse['m10'] / MatriceCentreMasse['m00'])
        centre_y = int(MatriceCentreMasse['m01'] / MatriceCentreMasse['m00'])
        return centre_x, centre_y

    def identifierForme(self, element):
        contoursForme, nomForme, couleurForme = element
        centreForme = self.trouverCentreForme(contoursForme)
        if (couleurForme == "TRESOR"):
            tresor = Tresor(centreForme)
            self.elementsCartographiques.append(tresor)
        else:
            ile = Ile(centreForme, couleurForme, nomForme)
            self.elementsCartographiques.append(ile)

    def trouverElementCartographiques(self):
        self.detectionIles = DetectionElementsCartographiques(self.imageCamera)
        self.detectionIles.detecterIles()
        self.detectionIles.detecterTresor()

        self.ilesIdentifiees = self.detectionIles.ilesIdentifiees
        self.tresorIdentifies = self.detectionIles.tresorIdentifies

        for element in self.ilesIdentifiees:
            self.identifierForme(element)
        for tresor in self.tresorIdentifies:
            self.identifierForme(tresor)

    def dessinerTrajet(self, trajet):
        point1 = None
        if (trajet == []):
            cv2.putText(self.imageCamera, 'Il n''existe aucun trajet!', (1000, 800), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            for point2 in trajet:
                if (point1 == None):
                    point1 = point2
                else:
                    cv2.arrowedLine(self.imageCamera,point2,point1,(0, 255, 0),5)
                    point1 = point2

    def dessinerElementCartographique(self):
        for element in self.elementsCartographiques:
            cv2.putText(self.imageCamera, element.forme, (element.centre_x-25, element.centre_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def dessinerDebutFinTrajet(self, debut, fin):
        x1, y1 = debut
        x2, y2 = fin
        cv2.putText(self.imageCamera, 'Debut', (x1-25, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.imageCamera, 'Fin', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    def afficherImage(self):
        cv2.imshow("Image", self.imageCamera)
        cv2.waitKey(0)