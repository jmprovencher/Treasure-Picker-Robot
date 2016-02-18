# import the necessary packages
import numpy as np
import cv2
from ElementCartographique import ElementCartographique
from Tresor import Tresor
from Ile import Ile


class DetectionIles(object):

    def __init__(self, image):
        self.imageCamera = image

        self.patronTriangle = cv2.imread('Image/triangle.png', 0)
        self.patronCercle = cv2.imread('Image/cercle.png', 0)
        self.patronCarre = cv2.imread('Image/carre.png', 0)
        self.patronPentagone = cv2.imread('Image/pentagone.png', 0)

        self.formesConnues = []
        self.ilesIdentifiees = []
        self.tresorIdentifies = []
        self.nombreFormes = 0
        self.nombreIles = 0

        #Intervalle clair, intervalle fonce
        self.intervalleRouge = np.array([100, 65, 200]), np.array([15, 0, 75]), "Rouge"
        self.intervalleBleu = np.array([255, 255, 102]), np.array([102, 102, 0]), "Bleu"
        self.intervalleJaune = np.array([51, 216, 242]), np.array([10, 120, 140]), "Jaune"
        self.intervalleVert = np.array([102, 255, 102]), np.array([0, 102, 0]), "Vert"

    def definirFormesConnues(self):
        """
        Definition d'un contour parfait pour chaque forme que le systeme devra detecter.
        Ces formes seront compares aux contours trouves par le systeme
        """

        precision, threshTriangle = cv2.threshold(self.patronTriangle, 127, 255, 0)
        precision, threshCercle = cv2.threshold(self.patronCercle, 127, 255, 0)
        precision, threshCarre = cv2.threshold(self.patronCarre, 127, 255, 0)
        precision, threshPentagone = cv2.threshold(self.patronPentagone, 127, 255, 0)

        # Recherche des contours
        _, contoursTriangle, _ = cv2.findContours(threshTriangle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntTriangle = contoursTriangle[0]
        _, contoursCercle, _ = cv2.findContours(threshCercle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCercle = contoursCercle[0]
        _, contoursCarre, _ = cv2.findContours(threshCarre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCarre = contoursCarre[0]
        _, contoursPentagone, _ = cv2.findContours(threshPentagone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntPentagone = contoursPentagone[0]

        # Ajoute les formes predeterminees dans une liste
        self.formesConnues.append(self.cntTriangle)
        self.formesConnues.append(self.cntCarre)
        self.formesConnues.append(self.cntCercle)
        self.formesConnues.append(self.cntPentagone)

    def detecterIles(self):
        self.detecterFormeCouleur(self.intervalleRouge)
        self.detecterFormeCouleur(self.intervalleBleu)
        self.detecterFormeCouleur(self.intervalleJaune)
        self.detecterFormeCouleur(self.intervalleVert)

    def detecterFormeCouleur(self, intervalleCouleur):
        """
        :param intervalleCouleur: intervalle des teintes de la couleur recherchee
        :return:
        """

        intervalleClair, intervalleFonce, couleurForme = intervalleCouleur

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        masqueCouleur = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)

        # Affiche l'image en noir et blanc
        #cv2.imshow(couleurForme, masqueCouleur)

        # Trouve les contours a l'aide du masque
        _, contoursCouleur, _ = cv2.findContours(masqueCouleur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursCouleur)):
            aire = cv2.contourArea(contoursCouleur[c])
            if ((aire < 1000) or (aire > 6000)):  # TODO: trouver la bonne valeur pour comparer
                index.append(c)

        if (len(index) > 0):
            contoursCouleur = np.delete(contoursCouleur, index)

        # print le nombre de forme trouver
        print "\nFormes %s : %d" % (couleurForme, len(contoursCouleur))

        # Identifier la forme
        for contoursForme in contoursCouleur:
            print cv2.contourArea(contoursForme)
            self.trouverForme(contoursForme, couleurForme)

    def trouverForme(self, contours, couleur):
        """
        Comparaison de chaque forme predefinie avec les contours de la forme detectee, afin d'obtenir un taux de compatibilite pour chaque forme
        :param contours: Un array contenant tous les contours de la forme
        :param couleur: La couleur correspondante aux contours
        """

        resultatsMatch = []
        resultatsMatch.append((cv2.matchShapes(contours, self.cntTriangle, 1, 0.0), contours, "Triangle"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCercle, 1, 0.0), contours, "Cercle"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntCarre, 1, 0.0), contours, "Carre"))
        resultatsMatch.append((cv2.matchShapes(contours, self.cntPentagone, 1, 0.0), contours, "Pentagone"))
        meilleurMatch = min(resultatsMatch)
        precision, contours, nomForme = meilleurMatch
        formeIdentifiee = contours, nomForme, couleur

        if (precision < 0.5):
            self.ilesIdentifiees.append(formeIdentifiee)
            self.nombreFormes += 1
            #self.identifierForme(meilleurMatch, couleur)
        else:
            print "Forme non conforme detectee"

        resultatsMatch.remove(meilleurMatch)

        deuxiemeMatch = min(resultatsMatch)
        precisionDeuxieme, _, nomFigure2 = deuxiemeMatch

        print "1er %s | Match %f" % (nomForme, precision)
        print "2e %s | Match %f" % (nomFigure2, precisionDeuxieme)
        print "---------------------------------------------------"



    def detecterTresor(self):
        """
        Detection des teintes de jaune venant de forme plus petites que les iles dans l'image
        """

        # Debut et fin de l'intervale de couleur jaune
        intervalleClair = np.array([37, 145, 145])  # Jimmy
        intervalleFoncer = np.array([6, 100, 100])  # Jimmy
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeTresorMasque = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)

        # Affiche l'image en noir et blanc
        #cv2.imshow("Masque Tresor", shapeTresorMasque)

        # Trouve les contours a l'aide du masque
        _, contoursTresor, _ = cv2.findContours(shapeTresorMasque.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursTresor)):
            aire = cv2.contourArea(contoursTresor[c])
            if (aire < 30 or aire > 150):  # TODO: trouver la bonne valeur pour comparer
                index.append(c)

        if (index != []):
            contoursTresor = np.delete(contoursTresor, index)

        # dessine par dessus les contours
        print "%d TRESORS " % (len(contoursTresor))

        # Identifier tresor
        for contours in contoursTresor:
            print cv2.contourArea(contours)
            formeTresor = contours, "Tresor", "TRESOR"
            self.tresorIdentifies.append(formeTresor)
            print "---------------------------------------------------"


    def getNombreFormes(self):
        """
        :return: Le nombre d'element rouge detecte
        """

        return self.nombreFormes

    def getNombreIles(self):
        """
        :return: Le nombre d'element bleu detecte
        """

        return self.nombreIles

    def getIlesIdentifiees(self):
        return self.ilesIdentifiees

    def getTresorsIdentifies(self):
        return self.tresorIdentifies