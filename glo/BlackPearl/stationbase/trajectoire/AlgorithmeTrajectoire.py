from __future__ import division
import heapq
from stationbase.trajectoire.Cellule import Cellule


class AlgorithmeTrajectoire:
    def __init__(self, grilleCellule):
        self.grilleCellule = grilleCellule
        self.heapOuvert = []
        heapq.heapify(self.heapOuvert)
        self.trajet = []
        self.fermer = set()
        self.depart = None
        self.departBuffer = None
        self.arriver = None
        self.cellulePlusPres = None

    def trouverTrajet(self, depart, arriver):
        self.trajet = []
        self.departBuffer = depart
        depart = self.trouverDebutBuffer(depart)
        self.setDepart(depart)
        self.setArriver(arriver)
        print 'arriver trajectoire'
        print self.arriver.x, self.arriver.y
        heapq.heappush(self.heapOuvert, (self.depart.priorite, self.depart))

        while len(self.heapOuvert):
            f, cellule = heapq.heappop(self.heapOuvert)
            self.fermer.add(cellule)
            if self.estArriver(cellule):
                self.simplifierTrajet()
                self.sectionnerTrajet()
                return self.trajet
            elif (self.cellulePlusPres is None) and (self.distanceBufferAcceptee(cellule)):
                self.cellulePlusPres = cellule
            elif self.distanceArriverCarre(cellule) < self.distanceArriverCarre(self.cellulePlusPres):
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
        self.sectionnerTrajet()
        return self.trajet

    def distanceBufferAcceptee(self, cellule):
        return (self.distanceAuCarre(cellule.x, cellule.y, self.arriver.x, self.arriver.y) >=
                (self.grilleCellule.rayonBuffer**2))

    def distanceArriverCarre(self, cellule):
        return self.distanceAuCarre(cellule.x, cellule.y, self.arriver.x, self.arriver.y)

    def sectionnerTrajet(self):
        i = 0
        while i < len(self.trajet)-1:
            debut = self.trajet[i]
            fin = self.trajet[i+1]
            if self.distanceAuCarre(debut[0], debut[1], fin[0], fin[1]) > 900:
                point = self.trouverPointMilieu(debut, fin)
                self.trajet = self.trajet[:i+1] + [point] + self.trajet[i+1:]
            else:
                i += 1

    def trouverPointMilieu(self, debut, fin):
        x = int(round(fin[0] + debut[0])/2)
        y = int(round(fin[1] + debut[1])/2)
        return x, y

    def distanceAuCarre(self, x, y, x2, y2):
        return self.grilleCellule.distanceAuCarre(x, y, x2, y2)

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

        self.trajet.append((self.depart.x, self.depart.y))
        if not (self.departBuffer[0] == self.depart.x and self.departBuffer[1] == self.depart.y):
            self.trajet.append(self.departBuffer)
        self.eliminerDetourInutile()

    def eliminerDetourInutile(self):
        longueurInitiale = 1
        longueurFinale = 0
        while longueurInitiale != longueurFinale:
            longueurInitiale = len(self.trajet)
            i = 0
            while len(self.trajet) > i+2:
                while (len(self.trajet) > i+2) and (self.ligneDroiteEstPossible(self.trajet[i], self.trajet[i+2])):
                    self.trajet.pop(i+1)
                i += 1
            longueurFinale = len(self.trajet)

    def ligneDroiteEstPossible(self, debut, fin):
        for ile in self.grilleCellule.listeIles:
            if self.ileTropPresALigne(ile, debut, fin):
                return False
        return True

    def ileTropPresALigne(self, ile, debut, fin):
        x1, y1 = debut
        x2, y2 = fin
        x3, y3 = (ile.centre_x, ile.centre_y)
        px = x2-x1
        py = y2-y1
        tmp = px*px + py*py
        u = ((x3 - x1) * px + (y3 - y1) * py) / float(tmp)
        if u > 1:
            u = 1
        elif u < 0:
            u = 0
        x = x1 + u * px
        y = y1 + u * py
        dx = x - x3
        dy = y - y3
        distCarre = dx*dx + dy*dy

        return distCarre < (int(round(self.grilleCellule.rayonBuffer * (
            self.grilleCellule.dimensionCrop[0]) / self.grilleCellule.dimensionReel[0])))**2

    def trouverDebutBuffer(self, depart):
        depart_x, depart_y = depart
        while not (depart_x % self.grilleCellule.incrementX == 0):
            depart_x += 1
        while not (depart_y % self.grilleCellule.incrementY == 0):
            depart_y += 1
        depart = self.grilleCellule.getCellule(depart_x, depart_y)
        depart1 = depart
        depart2 = depart
        depart3 = depart
        depart4 = depart
        listDepart = [depart1, depart2, depart3, depart4]
        while not depart.atteignable:
            if not listDepart[0].x >= 1600-25:
                if not listDepart[0].y >= 1200-25:
                    listDepart[0] = self.grilleCellule.getCellule(
                        listDepart[0].x+self.grilleCellule.incrementX, listDepart[0].y+self.grilleCellule.incrementY)
                if not listDepart[1].y <= 25:
                    listDepart[1] = self.grilleCellule.getCellule(
                        listDepart[1].x+self.grilleCellule.incrementX, listDepart[1].y-self.grilleCellule.incrementY)
            if not listDepart[2].x <= 25:
                if not listDepart[2].y >= 1200-25:
                    listDepart[2] = self.grilleCellule.getCellule(
                        listDepart[2].x-self.grilleCellule.incrementX, listDepart[2].y+self.grilleCellule.incrementY)
                if not listDepart[3].y <= 25:
                    listDepart[3] = self.grilleCellule.getCellule(
                        listDepart[3].x-self.grilleCellule.incrementX, listDepart[3].y-self.grilleCellule.incrementY)
            for dep in listDepart:
                if dep.atteignable:
                    depart = self.grilleCellule.getCellule(dep.x, dep.y)
                    break
        return depart.x, depart.y

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
        return (cellule.x == self.arriver.x) and (cellule.y == self.arriver.y)

    def estDepart(self, cellule):
        return (cellule.x == self.depart.x) and (cellule.y == self.depart.y)

