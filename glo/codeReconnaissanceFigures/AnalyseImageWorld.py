# import the necessary packages
import numpy as np
import cv2
from ElementCartographique import ElementCartographique
from Tresor import Tresor
from Ile import Ile

class AnalyseImageWorld(object):

    def __init__(self):
        self.m_image = cv2.imread('Image/test_imageTresor.png')
        self.m_triangle = cv2.imread('Image/triangle.png', 0)
        self.m_triangle2 = cv2.imread('Image/triangle2.png', 0)
        self.m_cercle = cv2.imread('Image/cercle.png', 0)
        self.m_carre = cv2.imread('Image/carre.png', 0)
        self.m_pentagone = cv2.imread('Image/pentagone.png', 0)
        self.formesConnues = []
        self.m_elementCartographiques = []
        self.definirFormesConnues()

    def trouverElement(self):

        # Affiche l'image initiale
        cv2.imshow("Image", self.m_image)

        self.cropPicture()
        self.blur()
        self.findTreasure()
        self.findBlue()
        self.findRed()
        self.findYellow()
        self.findGreen()

        # Affiche l'image apres detection
        cv2.imshow("Image2", self.m_image)

        # Permet de garder les images ouvertes
        cv2.waitKey(0)

    def cropPicture(self):
	# Hardcodage du crop #TODO: a verifier sur toute les tables
        #crop = self.m_image[220:1100,0:1600]
        crop = self.m_image[90:440,0:640]
        cv2.imwrite('Cropped.png',crop)
        self.m_image = cv2.imread('Cropped.png')

    def blur(self):
       blur = cv2.GaussianBlur(self.m_image,(5,5),0)
       cv2.imwrite('Cropped.png',blur)
       self.m_image = cv2.imread('Cropped.png')

    #Pour chaque forme, on definit un contour parfait qui sera compare aux contours trouves
    def definirFormesConnues(self):

        ret, threshTriangle = cv2.threshold(self.m_triangle, 127, 255,0)
        ret, threshCercle = cv2.threshold(self.m_cercle, 127, 255,0)
        ret, threshCarre = cv2.threshold(self.m_carre, 127, 255,0)
        ret, threshPentagone = cv2.threshold(self.m_pentagone, 127, 255,0)

        #Recherche des contours
        _, contoursTriangle, _ = cv2.findContours(threshTriangle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntTriangle = contoursTriangle[0]
        _, contoursCercle, _ = cv2.findContours(threshCercle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCercle = contoursCercle[0]
        _, contoursCarre, _ = cv2.findContours(threshCarre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntCarre = contoursCarre[0]
        _, contoursPentagone, _ = cv2.findContours(threshPentagone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cntPentagone = contoursPentagone[0]

        #Ajoute les formes predeterminees dans une liste
        self.formesConnues.append(self.cntTriangle)
        self.formesConnues.append(self.cntCarre)
        self.formesConnues.append(self.cntCercle)
        self.formesConnues.append(self.cntPentagone)

    #On compare les contours de chaque forme detectee avec nos formes predefinies pour
    #identifier la forme, soit la forme avec le meilleur ratio de compatibilite
    def trouverForme(self, c, couleur):

        classement = []
        classement.append((cv2.matchShapes(c,self.cntTriangle,1,0.0), c , "Triangle"))
        classement.append((cv2.matchShapes(c,self.cntCercle,1,0.0), c,  "Cercle"))
        classement.append((cv2.matchShapes(c,self.cntCarre,1,0.0), c,  "Carre"))
        classement.append((cv2.matchShapes(c,self.cntPentagone,1,0.0), c ,"Pentagone"))
        formeTrouvee = min(classement)
        precision, _, _ = formeTrouvee
        if (precision < 0.5):
            self.identifierForme(formeTrouvee, couleur)
        else:
            print "Forme non conforme detectee"


        classement.remove(formeTrouvee)
        deuxiemeTrouvee = min(classement)
        ret2, _ , text2 = deuxiemeTrouvee
        ret, c , text = formeTrouvee
        print "1er %s | Match %f" % (text, ret)
        print "2e %s | Match %f" % (text2, ret2)
        print "---------------------------------------------------"


    def identifierForme(self, formeTrouvee, couleur):
        font = cv2.FONT_HERSHEY_SIMPLEX
        _, c , text = formeTrouvee

        #Trouver centre de la forme
        M = cv2.moments(c)
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])

        # Afficher identification sur la photo
        cv2.putText(self.m_image,text,(centroid_x,centroid_y), font, 0.5,(0,0,0),1,cv2.LINE_AA)

        if (couleur == "TRESOR"):
            tresor = Tresor(centroid_x,centroid_y)
            self.m_elementCartographiques.append(tresor)
        else:
            ile = Ile(centroid_x,centroid_y,couleur,text)
            self.m_elementCartographiques.append(ile)


    def findRed(self):

	# Debut et fin de l'intervale de couleur rouge # TODO: trouver un meilleur intervale
        lower = np.array([36, 0, 129]) #970028
        upper = np.array([108, 40, 240]) #FF0044

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeRedMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskRouge", shapeRedMask)

        # Trouve les contours a l'aide du masque
        _, contoursRouge, _ = cv2.findContours(shapeRedMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursRouge)):
            aire = cv2.contourArea(contoursRouge[c])
            if ((aire < 100) or (aire > 900)): # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursRouge = np.delete(contoursRouge,index)

        # print le nombre de forme trouver
        print "\n%d FORMES ROUGE" % (len(contoursRouge))

        # Identifier la forme
        for c in contoursRouge:
            print cv2.contourArea(c)
            self.trouverForme(c,"ROUGE")

    def findBlue(self):

	# Debut et fin de l'intervale de couleur bleu
        upper = np.array([255, 255, 102]) #66FFFF
        lower = np.array([102, 102, 0]) #006666

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeBlueMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskBleu", shapeBlueMask)

        # Trouve les contours a l'aide du masque
        _, contoursBleu, _ = cv2.findContours(shapeBlueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursBleu)):
            aire = cv2.contourArea(contoursBleu[c])
            if (aire < 100 or aire > 1000): # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursBleu = np.delete(contoursBleu,index)

        # print le nombre de forme trouver
        print "\n%d FORMES BLEUES" % (len(contoursBleu))

        # Identifier la forme
        for c in contoursBleu:
            print cv2.contourArea(c)
            self.trouverForme(c,"BLEU")

    def findYellow(self):

	# Debut et fin de l'intervale de couleur jaune
        upper = np.array([51, 216, 242]) #F2D833
        lower = np.array([10, 120, 140]) #8C780A

        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeYellowMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskJaune", shapeYellowMask)

        # Trouve les contours a l'aide du masque
        _, contoursJaune, _ = cv2.findContours(shapeYellowMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursJaune)):
            aire = cv2.contourArea(contoursJaune[c])
            if (aire < 100 or aire > 1000): # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursJaune = np.delete(contoursJaune,index)

        # print le nombre de forme trouver
        print "\n%d FORMES JAUNE" % (len(contoursJaune))

        # Identifier la forme
        for c in contoursJaune:
            print cv2.contourArea(c)
            self.trouverForme(c,"JAUNE")

    def findGreen(self):

        # Debut et fin de l'intervale de couleur vert
        upper = np.array([102, 255, 102]) #66FF66
        lower = np.array([0, 102, 0]) #006600
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeGreenMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskVert", shapeGreenMask)

        # Trouve les contours a l'aide du masque
        _, contoursVert, _ = cv2.findContours(shapeGreenMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursVert)):
            aire = cv2.contourArea(contoursVert[c])
            if (aire < 100 or aire > 1000): # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursVert = np.delete(contoursVert,index)

        # print le nombre de forme trouver
        print "\n%d FORMES VERTES" % (len(contoursVert))

        # Identifier la forme
        for c in contoursVert:
            print cv2.contourArea(c)
            self.trouverForme(c,"VERT")

    def findTreasure(self):

        # Debut et fin de l'intervale de couleur jaune
        upper = np.array([37,145,145]) #Jimmy
        lower = np.array([6,100,100]) #Jimmy
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeTreasureMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskTreasure", shapeTreasureMask)

        # Trouve les contours a l'aide du masque
        _, contoursTreasure, _ = cv2.findContours(shapeTreasureMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # supprime les contours negligeable
        index = []
        for c in range(len(contoursTreasure)):
            aire = cv2.contourArea(contoursTreasure[c])
            if (aire < 10 or aire > 200): # TODO: trouver la bonne valeur pour comparer
                index += [c]

        if (index != []):
            contoursTreasure = np.delete(contoursTreasure,index)

        # dessine par dessus les contours
        print "%d TRESORS " % (len(contoursTreasure))

        # Identifier tresor
        for c in contoursTreasure:
            print cv2.contourArea(c)
            formeTresor = _, c ,"Tresor"
            self.identifierForme(formeTresor,"TRESOR")
            print "---------------------------------------------------"


    def getElementCartographiques(self):
        return self.m_elementCartographiques

    def ajouterElementTrouver(self, elementCarto):
        self.m_elementCartographiques += elementCarto



