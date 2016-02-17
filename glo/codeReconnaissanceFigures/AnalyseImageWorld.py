# import the necessary packages
import numpy as np
import cv2
from ElementCartographique import ElementCartographique
from Tresor import Tresor
from Ile import Ile


class AnalyseImageWorld(object):

    def __init__(self):
        # self.imageCamera = cv2.imread('Image/test_imageTresor.png')
        self.patronTriangle = cv2.imread('Image/triangle.png', 0)
        self.patronCercle = cv2.imread('Image/cercle.png', 0)
        self.patronCarre = cv2.imread('Image/carre.png', 0)
        self.patronPentagone = cv2.imread('Image/pentagone.png', 0)
        self.formesConnues = []
        self.elementsCartographiques = []
        self.definirFormesConnues()

        self.nombreFormeRouge = 0
        self.nombreFormeBleue = 0
        self.nombreFormeVerte = 0
        self.nombreFormeJaune = 0
        self.chargerImage('Image/test_imageTresor.png')

    def chargerImage(self, url):
        """
        Changement de l'image a traiter
        :param url: Le lien de l'image a charger dans le systeme de traitement
        """

        self.imageCamera = cv2.imread(url)

    def trouverElement(self):
        """
        Appelle toutes les fonctions de traitement visuel afin de trouver tous les elements
        """

        # cv2.imshow("Image", self.imageCamera)
        self.recadrerImage()
        self.estomperImage()
        self.detecterTresor()
        self.detecterBleu()
        self.detecterRouge()
        self.detecterJaune()
        self.detecterVert()

        # Affiche l'image apres detection
        cv2.imshow("Image2", self.imageCamera)

        # Permet de garder les images ouvertes
        cv2.waitKey(0)

    def recadrerImage(self):
        """
        Recadrage de l'image pour supprimer les zones inutiles qui se trouvent hors de la table
        """

        # Hardcodage du crop
        # TODO: a verifier sur toute les tables
        # crop = self.imageCamera[100:1000,0:1600]
        crop = self.imageCamera[90:440, 0:640]
        cv2.imwrite('Cropped.png', crop)
        self.imageCamera = cv2.imread('Cropped.png')

    def estomperImage(self):
        """
        On effectue un leger estompement de l'image afin de minimiser la fluctuation des pixels
        """

        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite('Cropped.png', blur)
        self.imageCamera = cv2.imread('Cropped.png')

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
        precision, _, _ = meilleurMatch

        if (precision < 0.5):
            self.identifierForme(meilleurMatch, couleur)
        else:
            print "Forme non conforme detectee"

        resultatsMatch.remove(meilleurMatch)
        precisionMeilleur, contours, nomFigure = meilleurMatch
        deuxiemeMatch = min(resultatsMatch)
        precisionDeuxieme, _, nomFigure2 = deuxiemeMatch

        print "1er %s | Match %f" % (nomFigure, precision)
        print "2e %s | Match %f" % (nomFigure2, precisionDeuxieme)
        print "---------------------------------------------------"

    def trouverCentreForme(self, contoursForme):
        """
        Detection du centre de la forme
        :param contoursForme: Contours de la forme
        :return: Un tuple correspondant aux coordonnees x,y du centre de la forme
        """

        M = cv2.moments(contoursForme)
        centre_x = int(M['m10'] / M['m00'])
        centre_y = int(M['m01'] / M['m00'])
        return centre_x, centre_y

    def identifierForme(self, meilleurMatch, couleur):
        """
        Identification de la forme detectee sur l'image
        :param meilleurMatch: Forme identifiee avec le plus haut taux de compatibilite
        :param couleur: La couleur de la forme identifiee
        """

        font = cv2.FONT_HERSHEY_SIMPLEX
        _, contoursForme, nomFigure = meilleurMatch

        centreForme = self.trouverCentreForme(contoursForme)
        # Afficher identification sur la photo
        cv2.putText(self.imageCamera, nomFigure, centreForme, font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        if (couleur == "TRESOR"):
            tresor = Tresor(centreForme)
            self.elementsCartographiques.append(tresor)
        else:
            ile = Ile(centreForme, couleur, nomFigure)
            self.elementsCartographiques.append(ile)

    def detecterRouge(self):
        """
        Detection des teintes de rouge dans l'image
        """

        # Debut et fin de l'intervale de couleur rouge # TODO: trouver un meilleur intervale
        intervalleFoncer = np.array([36, 0, 129])  # 970028
        intervalleClair = np.array([108, 40, 240])  # FF0044

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        masqueRouge = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)

        # Affiche l'image en noir et blanc
        #cv2.imshow("MaskRouge", masqueRouge)

        # Trouve les contours a l'aide du masque
        _, contoursRouge, _ = cv2.findContours(masqueRouge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursRouge)):
            aire = cv2.contourArea(contoursRouge[c])
            if ((aire < 100) or (aire > 900)):  # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursRouge = np.delete(contoursRouge, index)

        # print le nombre de forme trouver
        print "\n%d FORMES ROUGE" % (len(contoursRouge))

        # Identifier la forme
        for c in contoursRouge:
            print cv2.contourArea(c)
            self.trouverForme(c, "ROUGE")

        self.nombreFormeRouge = len(contoursRouge)

    def detecterBleu(self):
        """
        Detection des teintes de bleu dans l'image
        """

        # Debut et fin de l'intervale de couleur bleu
        intervalleClair = np.array([255, 255, 102])  # 66FFFF
        intervalleFoncer = np.array([102, 102, 0])  # 006666

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        masqueBleu = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)

        # Affiche l'image en noir et blanc
        #cv2.imshow("MaskBleu", masqueBleu)

        # Trouve les contours a l'aide du masque
        _, contoursBleu, _ = cv2.findContours(masqueBleu.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursBleu)):
            aire = cv2.contourArea(contoursBleu[c])
            if (aire < 100 or aire > 1000):  # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursBleu = np.delete(contoursBleu, index)

        # print le nombre de forme trouver
        print "\n%d FORMES BLEUES" % (len(contoursBleu))

        # Identifier la forme
        for c in contoursBleu:
            print cv2.contourArea(c)
            self.trouverForme(c, "BLEU")

        self.nombreFormeBleue = len(contoursBleu)

    def detecterJaune(self):
        """
        Detection des teintes de jaune dans l'image
        """

        # Debut et fin de l'intervale de couleur jaune
        intervalleClair = np.array([51, 216, 242])  # F2D833
        intervalleFoncer = np.array([10, 120, 140])  # 8C780A

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        masqueJaune = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)

        # Affiche l'image en noir et blanc
        #cv2.imshow("MaskJaune", masqueJaune)

        # Trouve les contours a l'aide du masque
        _, contoursJaune, _ = cv2.findContours(masqueJaune.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursJaune)):
            aire = cv2.contourArea(contoursJaune[c])
            if (aire < 100 or aire > 1000):  # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursJaune = np.delete(contoursJaune, index)

        # print le nombre de forme trouver
        print "\n%d FORMES JAUNE" % (len(contoursJaune))

        # Identifier la forme
        for c in contoursJaune:
            print cv2.contourArea(c)
            self.trouverForme(c, "JAUNE")
        self.nombreFormeJaune = len(contoursJaune)

    def detecterVert(self):
        """
        Detection des teintes de vert dans l'image
        """

        # Debut et fin de l'intervale de couleur vert
        intervalleClair = np.array([102, 255, 102])  # 66FF66
        intervalleFoncer = np.array([0, 102, 0])  # 006600
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        masqueVert = cv2.inRange(self.imageCamera, intervalleFoncer, intervalleClair)

        # Affiche l'image en noir et blanc
        #cv2.imshow("MaskVert", masqueVert)

        # Trouve les contours a l'aide du masque
        _, contoursVert, _ = cv2.findContours(masqueVert.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursVert)):
            aire = cv2.contourArea(contoursVert[c])
            if (aire < 100 or aire > 1000):  # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursVert = np.delete(contoursVert, index)

        # print le nombre de forme trouver
        print "\n%d FORMES VERTES" % (len(contoursVert))

        # Identifier la forme
        for c in contoursVert:
            print cv2.contourArea(c)
            self.trouverForme(c, "VERT")
        self.nombreFormeVerte = len(contoursVert)

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
            if (aire < 10 or aire > 200):  # TODO: trouver la bonne valeur pour comparer
                index.append(c)

        if (index != []):
            contoursTresor = np.delete(contoursTresor, index)

        # dessine par dessus les contours
        print "%d TRESORS " % (len(contoursTresor))

        # Identifier tresor
        for c in contoursTresor:
            print cv2.contourArea(c)
            formeTresor = _, c, "Tresor"
            self.identifierForme(formeTresor, "TRESOR")
            print "---------------------------------------------------"

    def getElementCartographiques(self):
        """
        :return: Retourne les elements cartographiques detectees par le systeme
        """

        return self.elementsCartographiques

    def ajouterElementTrouver(self, elementCarto):
        """
        Ajout d'un element cartographique dans la liste des elements cartographiques
        :param elementCarto: Un element cartographique
        """
        self.elementsCartographiques.append(elementCarto)

    def getNombreFormeRouge(self):
        """
        :return: Le nombre d'element rouge detecte
        """

        return self.nombreFormeRouge

    def getNombreFormeBleue(self):
        """
        :return: Le nombre d'element bleu detecte
        """

        return self.nombreFormeBleue

    def getNombreFormeJaune(self):
        """
        :return: Le nombre d'element jaune detecte
        """

        return self.nombreFormeJaune

    def getNombreFormeVerte(self):
        """
        :return: Le nombre d'element vert detecte
        """

        return self.nombreFormeVerte
