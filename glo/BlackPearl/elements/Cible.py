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
        #self.trouverIleCible()

    def trouverIleCible(self):
        posRobot = copy.deepcopy(self.carte.getRobotValide().getCentre())
        ilesPotentielle = self.carte.getIlesCorrespondantes(self.indice)
        distanceMin = 1000000000
        TresorsPossibles = self.trouverTresorsPossibles()
        for tresor in TresorsPossibles:
            trajetTresor = self.carte.getTrajectoire().trouverTrajet(posRobot, tresor.getCentre())
            distanceTresor = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.getTrajectoire().trouverTrajet(tresor.getCentre(), ile.getCentre())
                distanceIle = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetIle)
                distanceTotale = distanceTresor + distanceIle
                if distanceMin > distanceTotale:
                    distanceMin = distanceTotale
                    self.tresorChoisi = tresor
                    print 'TRESOR CHOISIE: ', tresor.centre_x, tresor.centre_y
                    self.ileChoisie = ile

    def trouverTresorsPossibles(self):
        tresorPossible = []
        for tresor in self.carte.getTresors():
            xTresor, yTresor = tresor.getCentre()
            for ile in self.carte.getIles():
                xIle, yIle = ile.getCentre()
                deltaXPix = abs(xTresor - xIle)
                deltaYPix = abs(yTresor - yIle)
                deltaX = self.carte.getTrajectoire().depPixelXACentimetre(deltaXPix)
                deltaY = self.carte.getTrajectoire().depPixelYACentimetre(deltaYPix)
                if deltaY > 50 and deltaX > 30:
                    tresorPossible.append(tresor)
        if not tresorPossible:
            tresorPossible.append(Tresor((0, 427)))

        return tresorPossible

    def getIleCible(self):
        return self.ileChoisie

    def getTresorCible(self):
        return self.tresorChoisi

    def getIndice(self):
        return self.indice







