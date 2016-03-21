# import the necessary packages
import heapq

from stationbase.trajectoire.Cellule import Cellule
from stationbase.trajectoire.GrilleCellule import GrilleCellule
import math


class AlgorithmeTrajectoire():
    def __init__(self, grilleCellule):
        self.grilleCellule = grilleCellule
        self.heapOuvert = []
        heapq.heapify(self.heapOuvert)
        self.trajet = []
        self.fermer = set()
        self.depart = None
        self.arriver = None
        self.cellulePlusPres = None

    def trouverTrajet(self, depart, arriver):
        self.trajet = []
        self.setDepart(depart)
        self.setArriver(arriver)
        heapq.heappush(self.heapOuvert, (self.depart.priorite, self.depart))

        while len(self.heapOuvert):
            f, cellule = heapq.heappop(self.heapOuvert)
            self.fermer.add(cellule)
            cellule.calculerDistance(self.arriver)
            if self.estArriver(cellule):
                self.simplifierTrajet()
                return self.trajet
            elif ((self.cellulePlusPres is None) and (self.distanceADestinationAuCarre(cellule.x, cellule.y, self.arriver.x, self.arriver.y) <= (self.grilleCellule.rayonBuffer*2)**2+1)):
                self.cellulePlusPres = cellule

            cellulesAdjacentes = self.grilleCellule.getCelluleAdjacentes(cellule)
            for adj in cellulesAdjacentes:
                if adj.atteignable and adj not in self.fermer:
                    if (adj.priorite, adj) in self.heapOuvert:
                        if adj.poid > cellule.poid + 10:
                            self.rafraichirCellule(adj, cellule)
                    else:
                        self.rafraichirCellule(adj, cellule)
                        heapq.heappush(self.heapOuvert, (adj.priorite, adj))

        self.arriver = self.cellulePlusPres
        self.simplifierTrajet()
        return self.trajet

    def distanceADestinationAuCarre(self, x, y, destX, destY):
        distanceX = destX - x
        distanceY = destY - y
        distanceX = self.pixelXACentimetre(distanceX)
        distanceY = self.pixelYACentimetre(distanceY)
        distanceCarre = distanceX**2 + distanceY**2
        return distanceCarre

    def simplifierTrajet(self):
        self.trajet = [(self.arriver.x, self.arriver.y)]
        cellule = self.grilleCellule.getCellule(self.arriver.x, self.arriver.y)
        depart_x = cellule.x - cellule.parent.x
        depart_y = cellule.y - cellule.parent.y

        while not self.estDepart(cellule.parent):
            temp = cellule
            cellule = cellule.parent
            if not ((temp.x - cellule.x == depart_x) and (temp.y - cellule.y == depart_y)):
                self.trajet.append((temp.x, temp.y))
                depart_x = temp.x - cellule.x
                depart_y = temp.y - cellule.y

        temp = cellule
        cellule = cellule.parent

        if not ((temp.x - cellule.x == depart_x) and (temp.y - cellule.y == depart_y)):
            self.trajet.append((temp.x, temp.y))
            depart_x = temp.x - cellule.x
            depart_y = temp.y - cellule.y

        self.trajet.append((self.depart.x, self.depart.y))
        self.eliminerDetourInutile()

    def eliminerDetourInutile(self):
        longueurInitiale = 1
        longueurFinale = 0
        while (longueurInitiale != longueurFinale):
            longueurInitiale = len(self.trajet)
            i = 0
            while (len(self.trajet) > i+2):
                while ((len(self.trajet) > i+2) and (self.ligneDroiteEstPossible(self.trajet[i], self.trajet[i+2]))):
                    self.trajet.pop(i+1)
                    print len(self.trajet)
                    print i
                i = i + 1
            longueurFinale = len(self.trajet)

    def ligneDroiteEstPossible(self, debut, fin):
        for ile in self.grilleCellule.listeIles:
            if (self.ileTropPresALigne(ile, debut, fin)):
                return False
        return True

    def ileTropPresALigne(self, ile, debut, fin):
        x1, y1 = debut
        x2, y2 = fin
        x3, y3 = (ile.centre_x, ile.centre_y)
        px = x2-x1
        py = y2-y1
        tmp = px*px + py*py
        u =  ((x3 - x1) * px + (y3 - y1) * py) / float(tmp)
        if u > 1:
            u = 1
        elif u < 0:
            u = 0
        x = x1 + u * px
        y = y1 + u * py
        dx = x - x3
        dy = y - y3
        dist = math.sqrt(dx*dx + dy*dy)

        return dist < int(round(self.grilleCellule.bufferIle * (self.grilleCellule.dimensionCrop[0]) / self.grilleCellule.dimensionReel[0]))

    def afficherTrajectoireDetailler(self):
        cellule = self.grilleCellule.getCellule(self.arriver.x, self.arriver.y)
        print "\n**************************"
        print "Trajectoire:"
        print "****************************\n"
        print "Arriver: cellule: %d, %d\n" % (self.arriver.x, self.arriver.y)
        if (self.trajet == []):
            print "Aucun trajet!"
        else:
            while not self.estDepart(cellule.parent):
                if (cellule.parent == None):
                    print "Aucun trajet!"
                else:
                    cellule = cellule.parent
                    print "cellule: %d, %d" % (cellule.x, cellule.y)
        print "\nDepart: cellule: %d, %d" % (self.depart.x, self.depart.y)

    def rafraichirCellule(self, celluleAdjacente, cellule):
        celluleAdjacente.poid = cellule.poid + 10
        celluleAdjacente.heuristique = celluleAdjacente.getHeuristique(self.arriver)
        celluleAdjacente.parent = cellule
        celluleAdjacente.priorite = celluleAdjacente.heuristique + celluleAdjacente.poid

    def setDepart(self, depart):
        depart_x, depart_y = depart
        while not (depart_x % self.grilleCellule.incrementX == 0):
            depart_x += 1
        while not (depart_y % self.grilleCellule.incrementY == 0):
            depart_y += 1
        self.depart = Cellule(depart_x, depart_y, True)

    def setArriver(self, arriver):
        arriver_x, arriver_y = arriver
        while not (arriver_x % self.grilleCellule.incrementX == 0):
            arriver_x += 1

        while not (arriver_y % self.grilleCellule.incrementY == 0):
            arriver_y += 1
        self.arriver = Cellule(arriver_x, arriver_y, True)

    def estArriver(self, cellule):
        if (cellule.x == self.arriver.x) and (cellule.y == self.arriver.y):
            return True
        else:
            return False

    def estDepart(self, cellule):
        if (cellule.x == self.depart.x) and (cellule.y == self.depart.y):
            return True
        else:
            return False
