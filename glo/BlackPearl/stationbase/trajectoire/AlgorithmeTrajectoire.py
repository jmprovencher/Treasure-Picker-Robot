from __future__ import division
import heapq
from stationbase.trajectoire.Cellule import Cellule
import copy
import math
from operator import itemgetter


class AlgorithmeTrajectoire:
    def __init__(self, grilleCellule):
        self.grilleCellule = grilleCellule
        self.heapOuvert = []
        heapq.heapify(self.heapOuvert)
        self.trajet = []
        self.rapport = 1.16
        self.coordonneeXMilieu = 813
        self.coordonneeYMilieu = 410
        self.fermer = set()
        self.depart = None
        self.departBuffer = None
        self.arriver = None
        self.cellulePlusPres = None

    def trouverTrajet(self, depart, arriver, type):
        self.trajet = []
        self.departBuffer = depart
        depart2 = self.trouverDebutBuffer(depart)
        self.setDepart(depart2)
        self.setArriver(arriver)
        heapq.heappush(self.heapOuvert, (self.depart.priorite, self.depart))

        while len(self.heapOuvert):
            f, cellule = heapq.heappop(self.heapOuvert)
            self.fermer.add(cellule)
            if self.estArriver(cellule):
                self.simplifierTrajet()
                self.sectionnerTrajet()
                return self.trajet
            elif self.cellulePlusPres is None:
                self.cellulePlusPres = cellule
            elif self.distanceArriverCarre(cellule) < self.distanceArriverCarre(self.cellulePlusPres):
                self.cellulePlusPres = cellule
                if type == 'ILE' and self.distanceArriverCarre(cellule) < 961:
                    break

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
        print 'arrivee:', self.arriver.x, self.arriver.y
        if type == 'ILE':
            tropLoin = 35
        else:
            tropLoin = 35
        if self.grilleCellule.rayonBuffer < 18:
            print 'introuvable'
            return [(-1, -1)]
        while self.grilleCellule.distanceAuCarre(self.arriver.x, self.arriver.y, arriver[0], arriver[1]) >= tropLoin**2:
            print 'nouvelle teration'
            self.grilleCellule.rayonBuffer -= 1
            print self.grilleCellule.rayonBuffer
            self.grilleCellule.initGrilleCellule(self.grilleCellule.listeIles)
            print 'nouvelle grille cellule'
            self.trajet = self.trouverTrajet(depart, arriver, type)
        if self.trajet is not None:
            self.simplifierTrajet()
            self.ajouterSecurite(type)
            self.enleverPointIdentique()
            self.sectionnerTrajet()
        print 'retour'
        print self.trajet
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
            if self.distanceAuCarre(debut[0], debut[1], fin[0], fin[1]) > 2500:
                point = self.trouverPointMilieu(debut, fin)
                self.trajet = self.trajet[:i+1] + [point] + self.trajet[i+1:]
            else:
                i += 1

    def enleverPointIdentique(self):
        i = 0
        while i < len(self.trajet)-3:
            debut1 = self.trajet[i]
            fin1 = self.trajet[i+1]
            debut2 = self.trajet[i+2]
            fin2 = self.trajet[i+3]
            if (debut1[0] == debut2[0] and fin1[0] == fin2[0] and debut1[1] == debut2[1] and fin1[1] == fin2[1]) or \
                    (debut1[0] == fin2[0] and fin1[0] == debut2[0] and debut1[1] == fin2[1] and fin1[1] == debut2[1]):
                self.trajet = self.trajet[:i+2] + self.trajet[i+4:]
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

    def ajouterSecurite(self, type):
        print 'ajouter securite'
        i = 0
        longueurTrajet = len(self.trajet)-1
        while i < longueurTrajet:
            print self.trajet
            point = self.trajet[i]
            ile1, ile2 = self.trouver2IlesPlusPres(point)
            if (self.distanceAuCarre(point[0], point[1], ile1.centre_x, ile1.centre_y) <= 30**2) and \
                    (self.distanceAuCarre(point[0], point[1], ile2.centre_x, ile2.centre_y) <= 30**2) and \
                    (self.distanceAuCarre(ile2.centre_x, ile2.centre_y, ile1.centre_x, ile1.centre_y) >= 30**2):
                point1, point2 = self.trouverNouveauPoint((ile1.centre_x, ile1.centre_y), (ile2.centre_x, ile2.centre_y))
                point1, point2 = self.ordonnerPointAjoute(point1, point2, self.trajet[i-1])
                debut = self.trajet[0]
                fin = self.trajet[-1]
                self.trajet = []
                trajet1 = copy.deepcopy(self.trouverTrajet(debut, point1, type))
                self.trajet = []
                trajet2 = copy.deepcopy(self.trouverTrajet(point2, fin, type))
                self.trajet = []
                self.trajet = trajet1 + trajet2
                i = longueurTrajet
            else:
                i += 1

    def ordonnerPointAjoute(self, point1, point2, pointP):
        distance1 = self.distanceAuCarre(point1[0], point1[1], pointP[0], pointP[1])
        distance2 = self.distanceAuCarre(point2[0], point2[1], pointP[0], pointP[1])
        if distance1 < distance2:
            return point1, point2
        else:
            return point2, point1

    def trouver2IlesPlusPres(self, point):
        list = []
        for ile in self.grilleCellule.listeIles:
            distance = self.distanceAuCarre(point[0], point[1], ile.centre_x, ile.centre_y)
            list.append((distance, copy.deepcopy(ile)))
        minimum = min(list, key=itemgetter(1))
        _, ile1 = minimum
        list.remove(minimum)
        minimum = min(list, key=itemgetter(1))
        _, ile2 = minimum
        return ile1, ile2

    def trouverNouveauPoint(self, point1, point2):
        facteur = 25
        MilieuX = int(round((point2[0] + point1[0])/2))
        MilieuY = int(round((point2[1] + point1[1])/2))
        deltaY = point2[1] - point1[1]
        deltaX = point2[0] - point1[0]
        if deltaX == 0:
            pointFinal1 = (MilieuX + self.grilleCellule.depCentimetreXAPixel(facteur), MilieuY)
            pointFinal2 = (MilieuX - self.grilleCellule.depCentimetreXAPixel(facteur), MilieuY)
        elif deltaY == 0:
            pointFinal1 = (MilieuX, MilieuY + self.grilleCellule.depCentimetreYAPixel(facteur))
            pointFinal2 = (MilieuX, MilieuY - self.grilleCellule.depCentimetreYAPixel(facteur))
        else:
            penteInit = deltaY/deltaX
            penteInverse = -1/penteInit
            teta = math.atan(penteInverse)
            pointFinal1 = (MilieuX + self.grilleCellule.depCentimetreXAPixel((facteur*math.cos(teta))), MilieuY + self.grilleCellule.depCentimetreYAPixel((facteur*math.sin(teta))))
            pointFinal2 = (MilieuX - self.grilleCellule.depCentimetreXAPixel((facteur*math.cos(teta))), MilieuY - self.grilleCellule.depCentimetreYAPixel((facteur*math.sin(teta))))
        return pointFinal1, pointFinal2

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
        arriver = self.correctionCentre(arriver)
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

    def correctionCentre(self, centre):
        xNonCorrige = centre[0]
        deltaX = xNonCorrige - self.coordonneeXMilieu
        xCorriger = int(round(self.coordonneeXMilieu + (deltaX * self.rapport)))
        yNonCorrige = centre[1]
        deltaY = yNonCorrige - self.coordonneeYMilieu
        yCorriger = int(round(self.coordonneeYMilieu + (deltaY * self.rapport)))

        return xCorriger, yCorriger

    def trouverOrientationDesire(self, debut, arriver):
        deltaX = arriver[0]-debut[0]
        deltaY = -1*(arriver[1]-debut[1])
        if not deltaX == 0:
            pente = deltaY/deltaX
        else:
            return 180

        if deltaY == 0 and deltaX < 0:
            angle = 180
        elif deltaY == 0 and deltaX > 0:
            angle = 0
        elif deltaX == 0 and deltaY > 0:
            angle = 90
        elif deltaX == 0 and deltaY < 0:
            angle = 270
        elif deltaX > 0 and deltaY > 0:
            angle = int(round(math.degrees(math.atan(pente))))
        elif deltaX > 0 and deltaY < 0:
            angle = 360 + int(round(math.degrees(math.atan(pente))))
        elif deltaX < 0:
            angle = 180 + int(round(math.degrees(math.atan(pente))))

        return angle

    def trouverCoordonneesSup(self, x, y):
        pointASup = []
        for point in self.trajet:
            if self.distanceAuCarre(x, y, point[0], point[1]) <= 30 and (point != (x, y)):
                pointASup.append(point)
        return pointASup

