import copy
from elements.Tresor import Tresor


class Cible:
    def __init__(self, args):
        self.carte = args[0]
        self.ileChoisie = None
        self.tresorChoisi = None
        self.possibilite = None
        self.tresorDansLeFond = False
        self.conteur = 0
        if len(args) == 1:
            self.indice = 'Bleu'
        else:
            self.indice = args[1]

    def trouverIleCible(self):
        print 'Trouver ile cible...'
        ilesPotentielle = self.carte.getIlesCorrespondantes(self.indice)
        distanceMin = 1000000000000
        tresorsPossibles = self.trouvertresorsPossibles()
        if self.tresorDansLeFond:
            self.possibilite = tresorsPossibles
        for tresor in tresorsPossibles:
            print 'test sur tresor'
            print tresor.getCentre()
            trajetTresor = self.carte.getTrajectoire().trouverTrajet(self.carte.getStationRecharge().getCentre(), tresor.getCentre(), 'TRESORE')
            distanceTresor = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.getTrajectoire().trouverTrajet(tresor.getCentre(), ile.getCentre(), 'ILE')
                distanceIle = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetIle)
                if distanceIle == -1:
                    continue
                distanceTotale = distanceTresor + distanceIle
                print 'Distance min', distanceMin
                print 'Distance totale', distanceTotale
                if distanceMin > distanceTotale:
                    distanceMin = distanceTotale
                    if not self.tresorDansLeFond:
                        self.tresorChoisi = tresor
                    self.ileChoisie = ile

        print 'Tresore choisie: ', self.tresorChoisi.centre_x, self.tresorChoisi.centre_y
        print 'Ile choisie: ', self.ileChoisie.forme, self.ileChoisie.couleur
        print 'Ile cible trouve'

    def trouvertresorsPossibles(self):
        tresorPossible = []
        for tresor in self.carte.getTresors():
            xTresor, yTresor = tresor.getCentre()
            accepte = True
            for ile in self.carte.getIles():
                xIle, yIle = ile.getCentre()
                deltaXPix = abs(xTresor - xIle)
                deltaYPix = abs(yTresor - yIle)
                deltaX = self.carte.getTrajectoire().depPixelXACentimetre(deltaXPix)
                deltaY = self.carte.getTrajectoire().depPixelYACentimetre(deltaYPix)
                if deltaY < 60 and deltaX < 30:
                    accepte = False
                    break
            if accepte:
                tresorPossible.append(tresor)
                print 'Tresor potentiel: ', tresor.centre_x, tresor.centre_y

        if not tresorPossible:
            self.tresorDansLeFond = True
            listeIle = self.carte.getIles()
            listetresors = [Tresor((0, 215)), Tresor((0, 430)), Tresor((0, 645))]
            for tresor in listetresors:
                if self.pasDileProche(tresor):
                    print 'Tresor potentiel: ', tresor.centre_x, tresor.centre_y
                    tresorPossible.append(tresor)

        return tresorPossible

    def pasDileProche(self, tresor):
        xTresor, yTresor = tresor.getCentre()
        accepte = True
        for ile in self.carte.getIles():
            xIle, yIle = ile.getCentre()
            deltaXPix = abs(xTresor - xIle)
            deltaYPix = abs(yTresor - yIle)
            deltaX = self.carte.getTrajectoire().depPixelXACentimetre(deltaXPix)
            deltaY = self.carte.getTrajectoire().depPixelYACentimetre(deltaYPix)
            if deltaY < 30 and deltaX < 60:
                accepte = False
                break

        return accepte

    def getIleCible(self):
        return self.ileChoisie

    def getTresorCible(self):
        return self.tresorChoisi

    def getIndice(self):
        return self.indice

    def setIndice(self, indice):
        self.indice = indice







