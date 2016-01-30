# import the necessary packages
import numpy as np
import cv2


class TraitementImage:

    def __init__(self):
        self.m_image = cv2.imread('Table3/2016-01-24-154511.jpg')
        #self.m_image = cv2.imread('noir.png')


    def test(self):

        # Affiche l'image initiale
        cv2.imshow("Image", self.m_image)

        self.cropPicture()
        self.m_image = cv2.imread('Cropped.png')

        self.findTreasure()
        self.findBlue()
        #self.findRed()
        #self.findYellow()
        self.findGreen()


        # Affiche l'image apres detection
        cv2.imshow("Image2", self.m_image)

        # Permet de garder les images ouvertes
        cv2.waitKey(0)

    def cropPicture(self):

        # Debut et fin de l'intervale de couleur blanche
        upper = np.array([255, 255, 255]) #FFFFFF
        lower = np.array([96, 96, 96]) #606060
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapewhiteMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskBlanc", shapewhiteMask)

        # Trouve les contours a l'aide du masque
        _, contoursTable, _ = cv2.findContours(shapewhiteMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print la fonction
        print "Picture cropped"

        # Trouve le plus grand contour
        airMax = 0
        temp = contoursTable[0]
        for c in contoursTable:
            if (cv2.contourArea(c) > airMax):
                temp = c
                airMax = cv2.contourArea(c)

        x,y,w,h = cv2.boundingRect(temp)

        crop = self.m_image[y:y+h+10,x:x+w]
        cv2.imwrite('Cropped.png',crop)

    def findRed(self):

        # Debut et fin de l'intervale de couleur rouge
        upper = np.array([65, 65, 255])
        lower = np.array([0, 0, 200])
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeRedMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskRouge", shapeRedMask)

        # Trouve les contours a l'aide du masque
        _, contoursRouge, _ = cv2.findContours(shapeRedMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print le nombre de forme trouver
        print "I found %d red shapes" % (len(contoursRouge))

        # dessine par dessus les contours
        for c in contoursRouge:
            cv2.drawContours(self.m_image, [c], -1, (0, 0, 255), 50)

    def findBlue(self):

        #different cyan avec eclairage : [020,126,140], [027, 123, 140], [021, 128, 148], [017, 122,140]
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
            if (cv2.contourArea(contoursBleu[c]) < 1000): # TODO: trouver la bonne valeur pour comparer
                index += [c]
        contoursBleu = np.delete(contoursBleu,index)

        # print le nombre de forme trouver
        print "I found %d blue shapes" % (len(contoursBleu))

        # Trouver la forme
        for c in contoursBleu:
            approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
            print len(approx)
            if len(approx)==3:
                print "Triangle"
                cv2.drawContours(self.m_image,[c],(255,0,0),2)
            elif len(approx)==4:
                print "Carre"
                cv2.drawContours(self.m_image,[c],0,(255,0,0),2)
            elif len(approx)==5:
                print "Pentagone"
                cv2.drawContours(self.m_image,[c],0,(255,0,0),2)
            elif len(approx) > 5:
                print "cercle"
                cv2.drawContours(self.m_image,[c],0,(255,0,0),2)

        # dessine par dessus les contours
        #for c in contoursBleu:
            #cv2.drawContours(self.m_image, [c], -1, (140, 126, 20), 20)

    def findYellow(self):

        # Debut et fin de l'intervale de couleur jaune
        upper = np.array([65, 255, 255])
        lower = np.array([0, 200, 200])
        # Retourne un masque binair (pixel=blanc (255, 255, 255) si elle est
        # dans l'intervalle et noir (0, 0, 0) dans le cas contraire)
        shapeYellowMask = cv2.inRange(self.m_image, lower, upper)

        # Affiche l'image en noir et blanc
        cv2.imshow("MaskJaune", shapeYellowMask)

        # Trouve les contours a l'aide du masque
        _, contoursJaune, _ = cv2.findContours(shapeYellowMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print le nombre de forme trouver
        print "I found %d yellow shapes" % (len(contoursJaune))

        # dessine par dessus les contours
        for c in contoursJaune:
            cv2.drawContours(self.m_image, [c], -1, (0, 255, 255), 50)

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
            if (cv2.contourArea(contoursVert[c]) < 1000): # TODO: trouver la bonne valeur pour comparer
                index += [c]
        contoursVert = np.delete(contoursVert,index)

        # print le nombre de forme trouver
        print "I found %d green shapes" % (len(contoursVert))

        # Trouver la forme
        for c in contoursVert:
            approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
            print len(approx)
            if len(approx)==3:
                print "Triangle"
                cv2.drawContours(self.m_image,[c],(255,255,0),2)
            elif len(approx)==4:
                print "Carre"
                cv2.drawContours(self.m_image,[c],0,(255,255,0),2)
            elif len(approx)==5:
                print "Pentagone"
                cv2.drawContours(self.m_image,[c],0,(255,255,0),2)
            elif len(approx) > 5:
                print "cercle"
                cv2.drawContours(self.m_image,[c],0,(255,255,0),2)

    def findTreasure(self):

        # Debut et fin de l'intervale de couleur jaune
        upper = np.array([51, 216, 242]) #F2D833
        lower = np.array([10, 120, 140]) #8C780A
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
            if (cv2.contourArea(contoursTreasure[c]) < 100): # TODO: trouver la bonne valeur pour comparer
                if (cv2.contourArea(contoursTreasure[c]) > 1000): # TODO: trouver la bonne valeur pour comparer
                    index += [c]
        contoursTreasure = np.delete(contoursTreasure,index)

        # print le nombre de forme trouver
        print "I found %d treasures" % (len(contoursTreasure))

        # dessine par dessus les contours
        for c in contoursTreasure:
            cv2.drawContours(self.m_image, [c], -1, (30, 121, 140), 20)



