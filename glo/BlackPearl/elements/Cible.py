import copy
from elements.Tresor import Tresor


class Cible:
    def __init__(self, args):
        self.carte = args[0]
        self.ileChoisie = None
        self.tresorChoisi = None
        if len(args) == 1:
            self.indice = 'Carre'
        else:
            self.indice = args[1]
        self.trouverIleCible()

    def trouverIleCible(self):
        posRobot = copy.deepcopy(self.carte.getRobotValide().getCentre())
        ilesPotentielle = self.carte.getIlesCorrespondantes(self.indice)
        distanceMin = 1000000
        TresorsPossibles = self.trouverTresorsPossibles()
        for tresor in TresorsPossibles:
            trajetTresor = self.carte.getTrajectoire().trouverTrajet(posRobot, tresor.getCentre())
            distanceTresor = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetTresor)
            for ile in ilesPotentielle:
                trajetIle = self.carte.getTrajectoire().trouverTrajet(posRobot, tresor.getCentre())
                distanceIle = self.carte.getTrajectoire().trouverLongueurTrajetCarre(trajetIle)
                distanceTotale = distanceTresor + distanceIle
                if distanceMin > distanceTotale:
                    distanceMin = distanceTotale
                    self.tresorChoisi = tresor
                    self.ileChoisie = ile

    def trouverTresorsPossibles(self):
        tresorPossible = []
        for tresor in self.carte.getTresor():
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
            tresorPossible.append(Tresor(0, 427))

        return tresorPossible

    def getIleCible(self):
        return self.ileChoisie

    def getTresorCible(self):
        return self.tresorChoisi







