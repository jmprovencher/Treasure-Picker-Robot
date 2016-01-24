# import the necessary packages
import numpy as np
import cv2


class TraitementImage:

    def __init__(self):
        self.m_image = cv2.imread('noir.png')

    def test(self):

        # Affiche l'image initiale
        cv2.imshow("Image", self.m_image)

        self.findRed()
        self.findBlue()
        self.findYellow()
        self.findGreen()

        # Affiche l'image avec les contours en plus
        cv2.imshow("Image2", self.m_image)

        # Permet de garder les images ouvertes
        cv2.waitKey(0)

    def findRed(self):

        # Debut et fin de l'intervale de couleur rouge
        upper = np.array([65, 65, 255])
        lower = np.array([0, 0, 200])
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeRedMask = cv2.inRange(self.m_image, lower, upper)

        # Trouve les contours a l'aide du masque
        _, contoursRouge, _ = cv2.findContours(shapeRedMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print le nombre de forme trouver
        print "I found %d red shapes" % (len(contoursRouge))

        # dessine par dessus les contours
        for c in contoursRouge:
            cv2.drawContours(self.m_image, [c], -1, (0, 0, 255), 50)

    def findBlue(self):

        # Debut et fin de l'intervale de couleur bleu
        upper = np.array([255, 65, 65])
        lower = np.array([200, 0, 0])
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeBlueMask = cv2.inRange(self.m_image, lower, upper)

        # Trouve les contours a l'aide du masque
        _, contoursBleu, _ = cv2.findContours(shapeBlueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print le nombre de forme trouver
        print "I found %d blue shapes" % (len(contoursBleu))

        # dessine par dessus les contours
        for c in contoursBleu:
            cv2.drawContours(self.m_image, [c], -1, (255, 0, 0), 50)

    def findYellow(self):

        # Debut et fin de l'intervale de couleur jaune
        upper = np.array([65, 255, 255])
        lower = np.array([0, 200, 200])
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeYellowMask = cv2.inRange(self.m_image, lower, upper)

        # Trouve les contours a l'aide du masque
        _, contoursJaune, _ = cv2.findContours(shapeYellowMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print le nombre de forme trouver
        print "I found %d yellow shapes" % (len(contoursJaune))

        # dessine par dessus les contours
        for c in contoursJaune:
            cv2.drawContours(self.m_image, [c], -1, (0, 255, 255), 50)

    def findGreen(self):

        # Debut et fin de l'intervale de couleur vert
        upper = np.array([65, 255, 65])
        lower = np.array([0, 200, 0])
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeGreenMask = cv2.inRange(self.m_image, lower, upper)

        # Trouve les contours a l'aide du masque
        _, contoursVert, _ = cv2.findContours(shapeGreenMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print le nombre de forme trouver
        print "I found %d green shapes" % (len(contoursVert))

        # dessine par dessus les contours
        for c in contoursVert:
            cv2.drawContours(self.m_image, [c], -1, (0, 255, 0), 50)

# Debut et fin de l'intervale de couleur
# lower = np.array([0, 0, 0])
# upper = np.array([15, 15, 15])
# Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est 
# dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
# shapeMask2 = cv2.inRange(image, lower, upper)

# Trouve les contours a l'aide du masque
# _, contours2, _ = cv2.findContours(shapeMask2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# print le nombre de forme trouver
# print "I found %d black shapes" % (len(contours2))

# Affiche l'image en noir et blanc
# cv2.imshow("Mask", shapeMask2)

# Affiche l'image avec les contours en plus
# cv2.imshow("Image2", image)

# reload l'image
# image2 = cv2.imread('findColors.png')

# for c in contours:
#    approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
#    print len(approx)
#    if len(approx)==3:
#        print "Triangle"
#        cv2.drawContours(image2,[c],0,255,2)
#    elif len(approx)==4:
#        print "Carre"
#        cv2.drawContours(image2,[c],0,(0,255,0),2)
#    elif len(approx)==5:
#        print "Pentagone"
#        cv2.drawContours(image2,[c],0,(0,0,255),2)
#    elif len(approx) > 5:
#        print "cercle"
#        cv2.drawContours(image2,[c],0,(255,255,0),2)
#
# Affiche l'image avec les contours en plus
# cv2.imshow("Image2", image2)
#
