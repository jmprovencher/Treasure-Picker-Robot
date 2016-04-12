from __future__ import division
from threading import Thread
import time


class TrouverTresorEtCible(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase

    def run(self):
        self.stationBase.threadAnalyseImageWorld.debuterDetectionTresors = True
        time.sleep(5)
        print 'Attendre l''indice'
        self.stationBase.attendreCible()
        self.stationBase.carte.cible.trouverIleCible()