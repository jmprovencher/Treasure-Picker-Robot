# import the necessary packages
import cv2
import numpy as np
import ConfigPath


class DetectionIles(object):
    def __init__(self, image, numeroTable):
        self.imageCamera = image
        self.numeroTable = numeroTable
        self.ilesIdentifiees = []
        self._definirPatronsFormes()

    def detecter(self):
        couleursIles = ['Rouge', 'Bleu', 'Jaune', 'Vert']
        for couleur in couleursIles:
            contoursIles, hierarchy = self.trouverContoursIles(couleur)
            contoursIles = self.eleminerCoutoursNegligeable(contoursIles, hierarchy)
            self.trouverIles(contoursIles, couleur)
        
    def trouverContoursIles(self, couleur):
        if (self.numeroTable == 5 or self.numeroTable == 6):
            if couleur == 'Rouge':
                intervalleFonce, intervalleClair = (np.array([15, 0, 75]), np.array([100, 65, 200]))
            elif couleur == 'Bleu':
                intervalleFonce, intervalleClair = (np.array([102, 102, 0]), np.array([255, 255, 102]))
            elif couleur == 'Jaune':
                intervalleFonce, intervalleClair = (np.array([0, 50, 50]), np.array([50, 255, 255]))
            elif couleur == 'Vert':
                intervalleFonce, intervalleClair = (np.array([0, 102, 0]), np.array([102, 255, 102]))
        elif (self.numeroTable == 1 or self.numeroTable == 2 or self.numeroTable == 3):
            if couleur == 'Rouge':
                intervalleFonce, intervalleClair = (np.array([0, 0, 70]), np.array([70, 50, 200]))
            elif couleur == 'Bleu':
                intervalleFonce, intervalleClair = (np.array([102, 102, 0]), np.array([255, 255, 102]))
            elif couleur == 'Jaune':
                intervalleFonce, intervalleClair = (np.array([0, 90, 91]), np.array([50, 194, 210]))
            elif couleur == 'Vert':
                intervalleFonce, intervalleClair = (np.array([0, 70, 0]), np.array([100, 200, 80]))
            
        masqueIles = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        _, contoursIles, hierarchy = cv2.findContours(masqueIles.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        return (contoursIles, hierarchy)
    
    def eleminerCoutoursNegligeable(self, contoursIles, hierarchy):
        contoursNegligeables = []

        for i in range(len(contoursIles)):
            aireContour = cv2.contourArea(contoursIles[i])
            indiceContourTrou = hierarchy[0][i][2]
            
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
        elif (len(contoursNegligeables) > 0):
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
            formeIdentifiee = contour, nomForme, couleur

            if (precision < 0.1):
                self.ilesIdentifiees.append(formeIdentifiee)

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



