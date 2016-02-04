# import the necessary packages
import numpy as np
import cv2


class TraitementImage:

    def __init__(self):
        self.m_image = cv2.imread('Image/test_image2.png')
        self.m_triangle = cv2.imread('Image/trianble.jpg')

    def test(self):

        # Affiche l'image initiale
        cv2.imshow("Image", self.m_image)

        self.cropPicture()
        self.m_image = cv2.imread('Cropped.png')

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
        crop = self.m_image[90:440,0:640]
        cv2.imwrite('Cropped.png',crop)

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
            if (cv2.contourArea(contoursRouge[c]) < 100): # TODO: trouver la bonne valeur pour comparer
                index += [c]
        contoursRouge = np.delete(contoursRouge,index)

        # print le nombre de forme trouver
        print "I found %d red shapes" % (len(contoursRouge))

        # Identifier la forme
        for c in contoursRouge:

	    # Trouver le centre
	    M = cv2.moments(c)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

	    # Trouver le nb de sommet
            approx = cv2.approxPolyDP(c,int(0.04*cv2.arcLength(c,True)),True)

	    # Identifier selon le nb de sommet
	    font = cv2.FONT_HERSHEY_SIMPLEX
            if len(approx)==3:
	        text = 'Triangle rouge'
            elif len(approx)==4:
                text = 'Carre rouge'
            elif len(approx)==5:
                text = 'Pentagone rouge'
            elif len(approx) > 5:
                text = 'Cercle rouge'
	    else:
		text = 'Erreur!'

	    # Afficher identification sur la photo 
	    cv2.putText(self.m_image,text,(centroid_x,centroid_y), font, 0.5,(0,0,0),1,cv2.LINE_AA)

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
            if (cv2.contourArea(contoursBleu[c]) < 100): # TODO: trouver la bonne valeur pour comparer
                index += [c]
        contoursBleu = np.delete(contoursBleu,index)

        # print le nombre de forme trouver
        print "I found %d blue shapes" % (len(contoursBleu))

        # Identifier la forme
        for c in contoursBleu:

	    # Trouver le centre
	    M = cv2.moments(c)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

	    # Trouver le nb de sommet
            approx = cv2.approxPolyDP(c,int(0.04*cv2.arcLength(c,True)),True)

	    # Identifier selon le nb de sommet
	    font = cv2.FONT_HERSHEY_SIMPLEX
            if len(approx)==3:
	        text = 'Triangle bleu'
            elif len(approx)==4:
                text = 'Carre bleu'
            elif len(approx)==5:
                text = 'Pentagone bleu'
            elif len(approx) > 5:
                text = 'Cercle bleu'
	    else:
		text = 'Erreur!'

	    # Afficher identification sur la photo 
	    cv2.putText(self.m_image,text,(centroid_x,centroid_y), font, 0.5,(0,0,0),1,cv2.LINE_AA)

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
            if (cv2.contourArea(contoursJaune[c]) < 100): # TODO: trouver la bonne valeur pour comparer
                index += [c]
        contoursJaune = np.delete(contoursJaune,index)

        # print le nombre de forme trouver
        print "I found %d yellow shapes" % (len(contoursJaune))

        # Identifier la forme
        for c in contoursJaune:

	    # Trouver le centre
	    M = cv2.moments(c)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

	    # Trouver le nb de sommet
            approx = cv2.approxPolyDP(c,int(0.04*cv2.arcLength(c,True)),True)

	    # Identifier selon le nb de sommet
	    font = cv2.FONT_HERSHEY_SIMPLEX
            if len(approx)==3:
	        text = 'Triangle jaune'
            elif len(approx)==4:
                text = 'Carre jaune'
            elif len(approx)==5:
                text = 'Pentagone jaune'
            elif len(approx) > 5:
                text = 'Cercle jaune'
	    else:
		text = 'Erreur!'

	    # Afficher identification sur la photo 
	    cv2.putText(self.m_image,text,(centroid_x,centroid_y), font, 0.5,(0,0,0),1,cv2.LINE_AA)

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
            if (cv2.contourArea(contoursVert[c]) < 100): # TODO: trouver la bonne valeur pour comparer
                index += [c]
        contoursVert = np.delete(contoursVert,index)

        # print le nombre de forme trouver
        print "I found %d green shapes" % (len(contoursVert))

        # Identifier la forme
        for c in contoursVert:

	    # Trouver le centre
	    M = cv2.moments(c)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

	    # Trouver le nb de sommet
            approx = cv2.approxPolyDP(c,int(0.04*cv2.arcLength(c,True)),True)

	    # Identifier selon le nb de sommet
	    font = cv2.FONT_HERSHEY_SIMPLEX
            if len(approx)==3:
	        text = 'Triangle vert'
            elif len(approx)==4:
                text = 'Carre vert'
            elif len(approx)==5:
                text = 'Pentagone vert'
            elif len(approx) > 5:
                text = 'Cercle vert'
	    else:
		text = 'Erreur!'

	    # Afficher identification sur la photo 
	    cv2.putText(self.m_image,text,(centroid_x,centroid_y), font, 0.5,(0,0,0),1,cv2.LINE_AA)

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
            if ((cv2.contourArea(contoursTreasure[c]) < 10) or (cv2.contourArea(contoursTreasure[c]) > 200)): # TODO: trouver la bonne valeur pour comparer
                    index += [c]
        contoursTreasure = np.delete(contoursTreasure,index)

        # print le nombre de forme trouver
        print "I found %d treasures" % (len(contoursTreasure))

        # dessine par dessus les contours
        for c in contoursTreasure:
            cv2.drawContours(self.m_image, [c], -1, (30, 121, 140), 20)



