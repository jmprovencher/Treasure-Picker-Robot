from stationbase.trajectoire.Trajectoire import Trajectoire
from elements.StationRecharge import StationRecharge
from elements.Cible import Cible
import time
import copy


class Carte:
    def __init__(self):
        self.listeIles = []
        self.listeTresors = []
        self.robot = None
        self.cible = None
        self.stationRecharge = StationRecharge()
        self.trajectoire = Trajectoire()

    def getIles(self):
        return self.listeIles

    def getIlesCorrespondantes(self, informationIleCible):
        retour = []
        for ile in self.listeIles:
            if ile.couleur.lower() == informationIleCible.lower() or ile.forme.lower() == informationIleCible.lower():
                retour.append(ile)
        return retour

    def setIles(self, listIles):
        self.listeIles = listIles

    def getTresors(self):
        return self.listeTresors

    def setTresors(self, listTresors):
        self.listeTresors = listTresors

    def getRobot(self):
        return self.robot

    def getRobotValide(self):
        while self.robot is None:
            time.sleep(0.01)
        return copy.deepcopy(self.robot)

    def setRobot(self, robot):
        self.robot = robot

    def getTrajectoire(self):
        return self.trajectoire

    def getCible(self):
        return self.cible

    def setCible(self, cible):
        self.cible = cible

    def getStationRecharge(self):
        return self.stationRecharge




