import cv2
import numpy as np
import ConfigPath
from stationbase.vision.InfoTable import InfoTable
from stationbase.vision.Detection import Detection
from elements.Ile import Ile


class DetectionIles(Detection):
    def __init__(self, image, numeroTable):
        Detection.__init__(self, image, numeroTable)
        self.ilesIdentifiees = []
        self._definirPatronsFormes()

    def detecter(self):
        couleursIles = ['Rouge', 'Bleu', 'Jaune', 'Vert']
        for couleur in couleursIles:
            contoursIles, hierarchie = self.trouverContoursIles(couleur)
            contoursIles = self.eleminerCoutoursNegligeable(contoursIles, hierarchie)
            self.trouverIles(contoursIles, couleur)
        
    def trouverContoursIles(self, couleur):
        intervalleFonce, intervalleClair = InfoTable(couleur, self.numeroTable).getIntervalle()
        masqueIles = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursIles, hierarchie = cv2.findContours(masqueIles.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        return contoursIles, hierarchie
    
    def eleminerCoutoursNegligeable(self, contoursIles, hierarchie):
        contoursNegligeables = []

        for i in range(len(contoursIles)):
            aireContour = cv2.contourArea(contoursIles[i])
            indiceContourTrou = hierarchie[0][i][2]
            
            if indiceContourTrou >= 0:  # Signifie que le contour possede un trou
                aireTrouContour = cv2.contourArea(contoursIles[indiceContourTrou])
            else:
                aireTrouContour = 0
                
            if (aireContour < 2000) or (aireContour > 6000):
                contoursNegligeables.append(i)
            elif aireTrouContour > 50:
                contoursNegligeables.append(i)

        if len(contoursIles) == len(contoursNegligeables):
            contoursIles = []
        elif contoursNegligeables:
            contoursIles = np.delete(contoursIles, contoursNegligeables)

        return contoursIles

    def trouverIles(self, contoursIles, couleur):
        for contour in contoursIles:
            resultatsMatch = []
            resultatsMatch.append((cv2.matchShapes(contour, self.cntTriangle, 1, 0.0), contour, 'Triangle'))
            resultatsMatch.append((cv2.matchShapes(contour, self.cntCercle, 1, 0.0), contour, 'Cercle'))
            resultatsMatch.append((cv2.matchShapes(contour, self.cntCarre, 1, 0.0), contour, 'Carre'))
            resultatsMatch.append((cv2.matchShapes(contour, self.cntPentagone, 1, 0.0), contour, 'Pentagone'))
            meilleurMatch = min(resultatsMatch)
            precision, contour, nomForme = meilleurMatch

            if precision < 0.1:
                centre = self.trouverCentre(contour)
                self.ilesIdentifiees.append(Ile(centre, couleur, nomForme))

            if couleur == 'Rouge':
                print 'Centre rouge'
                print centre

    def getIlesIdentifiees(self):
        return self.ilesIdentifiees

    def _definirPatronsFormes(self):
        patronTriangle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/triangle.png'), 0)
        precision, threshTriangle = cv2.threshold(patronTriangle, 127, 255, 0)
        _, contoursTriangle, _ = cv2.findContours(threshTriangle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntTriangle = contoursTriangle[0]
        
        patronCercle = cv2.imread(ConfigPath.Config().appendToProjectPath('images/cercle.png'), 0)
        precision, threshCercle = cv2.threshold(patronCercle, 127, 255, 0)
        _, contoursCercle, _ = cv2.findContours(threshCercle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCercle = contoursCercle[0]
        
        patronCarre = cv2.imread(ConfigPath.Config().appendToProjectPath('images/carre.png'), 0)
        precision, threshCarre = cv2.threshold(patronCarre, 127, 255, 0)
        _, contoursCarre, _ = cv2.findContours(threshCarre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCarre = contoursCarre[0]
        
        patronPentagone = cv2.imread(ConfigPath.Config().appendToProjectPath('images/pentagone.png'), 0)
        precision, threshPentagone = cv2.threshold(patronPentagone, 127, 255, 0)
        _, contoursPentagone, _ = cv2.findContours(threshPentagone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntPentagone = contoursPentagone[0]



