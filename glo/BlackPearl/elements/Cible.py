import copy
from elements.Tresor import Tresor
import time


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
            self.ileChoisie = self.carte.getIlesCorrespondantes(self.indice)[0]
        else:
            self.indice = args[1]

    def trouverIleCible(self):
        print 'Trouver ile cible...'
        ilesPotentielle = self.carte.getIlesCorrespondantes(self.indice)
        distanceMin = 1000000000000
        time.sleep(10)
        tresorsPossibles = self.trouvertresorsPossibles()
        self.possibilite = tresorsPossibles
        tmp = self.possibilite
        print 'init list'
        print self.possibilite
        print self.conteur
        for i in range(len(tresorsPossibles)):
            print 'test sur tresor'
            print tresorsPossibles[i].getCentre()
            trajetTresor = self.carte.getTrajectoire().trouverTrajet(self.carte.getStationRecharge().getCentre(), tresorsPossibles[i].getCentre(), 'TRESORE')
            distanceTresor = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.getTrajectoire().trouverTrajet(tresorsPossibles[i].getCentre(), copy.deepcopy(ile.getCentre()), 'ILE')
                distanceIle = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetIle)
                if distanceIle == -1:
                    continue
                distanceTotale = distanceTresor + distanceIle
                print 'Distance min', distanceMin
                print 'Distance totale', distanceTotale
                if distanceMin > distanceTotale:
                    distanceMin = distanceTotale
                    tresorChoisi = copy.deepcopy(tresorsPossibles[i])
                    self.tresorChoisi = tresorChoisi
                    self.ileChoisie = copy.deepcopy(ile)
                    print 'changement 1'
                    print self.possibilite
                    print self.conteur
        if self.ileChoisie is None:
            self.ileChoisie = ilesPotentielle[0]
        print 'Tresore choisie: ', self.tresorChoisi.centre_x, self.tresorChoisi.centre_y
        print 'Ile choisie: ', self.ileChoisie.forme, self.ileChoisie.couleur
        print 'Ile cible trouve'

    def trouvertresorsPossibles(self):
        tresorPossible = []
        print len(self.carte.getTresors())
        for tresor in self.carte.getTresors():
            xTresor, yTresor = tresor.getCentre()
            accepte = True
            for ile in self.carte.getIles():
                print 'tresor normal'
                xIle, yIle = ile.getCentre()
                deltaXPix = abs(xTresor - xIle)
                deltaYPix = abs(yTresor - yIle)
                deltaX = self.carte.getTrajectoire().depPixelXACentimetre(deltaXPix)
                deltaY = self.carte.getTrajectoire().depPixelYACentimetre(deltaYPix)
                if deltaY < 50 and deltaX < 30:
                    print 'tresor normal accepter'
                    accepte = False
                    break
            if accepte:
                tresorPossible.append(tresor)
                print 'Tresor potentiel: ', tresor.centre_x, tresor.centre_y

        if not tresorPossible:
            print 'Tresor potentie'
            self.tresorDansLeFond = True
            listeIle = self.carte.getIles()
            listetresors = [Tresor((0, 215)), Tresor((0, 430)), Tresor((0, 645))]
            for tresor in listetresors:
                if self.pasDileProche(tresor):
                    print 'Tresor potentiel: ', tresor.centre_x, tresor.centre_y
                    tresorPossible.append(tresor)
            print 'fond : ', len(tresorPossible)

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
        #print self.conteur
        #print self.possibilite[self.conteur].getCentre()[0]
        #print self.possibilite[self.conteur].getCentre()[1]
        return self.tresorChoisi

    def getIndice(self):
        return self.indice

    def setIndice(self, indice):
        self.indice = indice







