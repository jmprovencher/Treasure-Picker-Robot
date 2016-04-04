from __future__ import division
from stationbase.trajectoire.Cellule import Cellule


class GrilleCellule:
    def __init__(self):
        self.listeCellules = []
        self.resolution = (1600, 1200)
        self.dimensionCrop = (1600, 855)
        self.dimensionReel = (230, 115)
        self.incrementX = int((self.dimensionCrop[0]) / self.dimensionReel[0])
        self.incrementY = int((self.dimensionCrop[1]) / self.dimensionReel[1])
        self.rayonBuffer = 30
        self.distanceMur = 25
        self.distPerteDeVueRobot = 5
        self.listeIles = None

    def initGrilleCellule(self, listeIles):
        self.listeIles = listeIles
        for x in range(0, self.dimensionCrop[0], self.incrementX):
            for y in range(0, self.dimensionCrop[1], self.incrementY):
                    self.listeCellules.append(Cellule(x, y, self.estAtteignable(x, y)))
                
    def depPixelXACentimetre(self, pix):
        return pix * (self.dimensionReel[0] / self.dimensionCrop[0])
    
    def depPixelYACentimetre(self, pix):
        return pix * (self.dimensionReel[1] / self.dimensionCrop[1])

    def depCentimetreYAPixel(self, cent):
        return int(round(cent * (self.dimensionCrop[1]) / self.dimensionReel[1]))

    def depCentimetreXAPixel(self, cent):
        return int(round(cent * (self.dimensionCrop[0]) / self.dimensionReel[0]))
    
    def distanceAuCarre(self, x, y, x2, y2):
        distanceX = x2 - x
        distanceY = y2 - y
        distanceX = self.depPixelXACentimetre(distanceX)
        distanceY = self.depPixelYACentimetre(distanceY)
        distanceCarre = distanceX**2 + distanceY**2
        return int(round(distanceCarre))
                
    def estAtteignable(self, x, y):
        if self.xInvalide(x) or self.yInvalide(y):
            return False
        else:
            for ile in self.listeIles:
                if self.distanceAuCarre(x, y, ile.getX(), ile.getY()) <= self.rayonBuffer**2:
                    return False
            return True

    def xInvalide(self, x):
        return ((x >= self.dimensionCrop[0]-self.depCentimetreXAPixel(self.distPerteDeVueRobot)) or
            (x <= self.depCentimetreXAPixel(self.distPerteDeVueRobot)))

    def yInvalide(self, y):
        return ((y <= self.depCentimetreYAPixel(self.distanceMur)) or
                (y >= self.dimensionCrop[1]-self.depCentimetreYAPixel(self.distanceMur)))

    def getCellule(self, x, y):
        return self.listeCellules[
            (x // self.incrementX) * (self.dimensionCrop[1] // self.incrementY + 1) + (y // self.incrementY)]

    def getCelluleAdjacentes(self, cellule):
        listCellules = []

        if cellule.x < self.dimensionCrop[0] - self.incrementX:
            listCellules.append(self.getCellule(cellule.x + self.incrementX, cellule.y))

        if cellule.y >= 0 + self.incrementY:
            listCellules.append(self.getCellule(cellule.x, cellule.y - self.incrementY))

        if cellule.x >= 0 + self.incrementX:
            listCellules.append(self.getCellule(cellule.x - self.incrementX, cellule.y))

        if cellule.y < self.dimensionCrop[1] - self.incrementY:
            listCellules.append(self.getCellule(cellule.x, cellule.y + self.incrementY))

        if ((cellule.x < self.dimensionCrop[0] - self.incrementX) and (
                    cellule.y < self.dimensionCrop[1] - self.incrementY)):
            listCellules.append(self.getCellule(cellule.x + self.incrementX, cellule.y + self.incrementY))

        if (cellule.x >= 0 + self.incrementX) and (cellule.y >= 0 + self.incrementY):
            listCellules.append(self.getCellule(cellule.x - self.incrementX, cellule.y - self.incrementY))

        if (cellule.x < self.dimensionCrop[0] - self.incrementX) and (cellule.y >= 0 + self.incrementY):
            listCellules.append(self.getCellule(cellule.x + self.incrementX, cellule.y - self.incrementY))

        if (cellule.x >= 0 + self.incrementX) and (cellule.y < self.dimensionCrop[1] - self.incrementY):
            listCellules.append(self.getCellule(cellule.x - self.incrementX, cellule.y + self.incrementY))

        return listCellules
