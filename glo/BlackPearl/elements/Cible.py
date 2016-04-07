import copy
from elements.Tresor import Tresor


class Cible:
    def __init__(self, args):
        self.carte = args[0]
        self.ileChoisie = None
        self.tresorChoisi = None
        if len(args) == 1:
            self.indice = 'Bleu'
        else:
            self.indice = args[1]

    def trouverIleCible(self):
        print 'Trouver ile cible...'
        ilesPotentielle = self.carte.getIlesCorrespondantes(self.indice)
        distanceMin = 1000000000000
        tresorsPossibles = self.trouvertresorsPossibles()
        for tresor in tresorsPossibles:
            print 'test sur tresor'
            print tresor.getCentre()
            trajetTresor = self.carte.getTrajectoire().trouverTrajet(self.carte.getStationRecharge().getCentre(), tresor.getCentre())
            distanceTresor = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.getTrajectoire().trouverTrajet(tresor.getCentre(), ile.getCentre())
                distanceIle = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetIle)
                distanceTotale = distanceTresor + distanceIle
                if distanceMin > distanceTotale:
                    distanceMin = distanceTotale
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
                if deltaY < 40 and deltaX < 25:
                    accepte = False
                    break
            if accepte:
                tresorPossible.append(tresor)
                print 'Tresor potentiel: ', tresor.centre_x, tresor.centre_y

        if not tresorPossible:
            tresorPossible.append(Tresor((0, 427)))
            print 'Aucun tresor possible... Tresor par defaut (0, 427)'

        return tresorPossible

    def getIleCible(self):
        return self.ileChoisie

    def getTresorCible(self):
        return self.tresorChoisi

    def getIndice(self):
        return self.indice

    def setIndice(self, indice):
        self.indice = indice







