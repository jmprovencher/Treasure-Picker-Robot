# import the necessary packages
import cv2
import ConfigPath
from elements.Ile import Ile
from elements.Tresor import Tresor
from stationbase.vision.DetectionIles import DetectionIles
from stationbase.vision.DetectionRobot import DetectionRobot
from stationbase.vision.DetectionTable import DetectionTable
from stationbase.vision.DetectionTresors import DetectionTresors


class AnalyseImageWorld(object):
    def __init__(self):
        self.elementsCartographiques = []
        self.detectionEffectuee = False
        self.tresorIdentifies = []
        self.ilesIdentifiees = []
        self.police = cv2.FONT_HERSHEY_SIMPLEX
        self.detectionIles = None

    def chargerImage(self, image):
        self.imageCamera = image
        # self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath(image))
        self.recadrerImage()
        self.estomperImage()

    def recadrerImage(self):
        self.detectionTable = DetectionTable(self.imageCamera)
        y = self.detectionTable.detecterCentreYCarreVert()
        crop = self.imageCamera[y - 425:y + 425, 0:1600]
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), crop)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))

    def estomperImage(self):
        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite(ConfigPath.Config().appendToProjectPath('Cropped.png'), blur)
        self.imageCamera = cv2.imread(ConfigPath.Config().appendToProjectPath('Cropped.png'))

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

    def trouverElementsCartographiques(self):
        self.elementsCartographiques = []
        ########################################
        #cv2.imshow('Image Analysee', self.imageCamera)
        if (self.detectionEffectuee == False):
            print("Detection des iles et tresors....")
            self.detectionIles = DetectionIles(self.imageCamera)
            self.detectionTresors = DetectionTresors(self.imageCamera)
            self.detectionIles.detecter()
            self.detectionTresors.detecter()
            self.ilesIdentifiees = self.detectionIles.ilesIdentifiees
            self.tresorIdentifies = self.detectionTresors.tresorIdentifies
            self.detectionEffectuee = True
        if (self.detectionEffectuee == True):
            self.detectionRobot = DetectionRobot(self.imageCamera)
            print("Detection robot....")

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
        cv2.imshow('Afficher Image', self.imageCamera)
