import cv2
import numpy as np
from stationbase.vision.IntervalleCouleur import IntervalleCouleur
from stationbase.vision.Detection import Detection
from elements.Tresor import Tresor


class DetectionTresors(Detection):
    def __init__(self, image, numeroTable):
        Detection.__init__(self, image, numeroTable)
        self.tresorIdentifies = []

    def detecter(self):
        contoursTresors = self.trouverContoursTresors()
        contoursTresors = self.eleminerCoutoursNegligeables(contoursTresors)
        self.trouverTresors(contoursTresors)
        self.eliminerTresorsImpossibles()

    def trouverContoursTresors(self):
        intervalleFonce, intervalleClair = IntervalleCouleur('Tresor', self.numeroTable).getIntervalle()
        masqueTresors = cv2.inRange(self.imageCamera, intervalleClair, intervalleFonce)
        _, contoursTresors, _ = cv2.findContours(masqueTresors.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contoursTresors

    def eleminerCoutoursNegligeables(self, contoursTresors):
        contoursNegligeables = []

        for i in range(len(contoursTresors)):
            aire = cv2.contourArea(contoursTresors[i])
            if aire < 30 or aire > 150:
                contoursNegligeables.append(i)

        if len(contoursTresors) == len(contoursNegligeables):
            contoursTresors = []
        elif not contoursNegligeables:
            contoursTresors = np.delete(contoursTresors, contoursNegligeables)

        return contoursTresors

    def trouverTresors(self, contoursTresors):
        if len(contoursTresors) > 0:
            for contour in contoursTresors:
                centre = self.trouverCentre(contour)
                self.tresorIdentifies.append(Tresor(centre))

    def eliminerTresorsImpossibles(self):
        tresorsImpossible = []

        for i in range(len(self.tresorIdentifies)):
            x, y = self.tresorIdentifies[i].getCentre()
            if self.numeroTable == 1:
                if (y > 45) or (y < 750) or (x > 1321):
                    tresorsImpossible.append(i)
            elif self.numeroTable == 2 or self.numeroTable == 3:
                if (y > 45) or (y < 810) or (x > 1347):
                    tresorsImpossible.append(i)
            elif self.numeroTable == 5 or self.numeroTable == 6:
                if (y > 30) or (y < 810) or (x > 1321):
                    tresorsImpossible.append(i)

        if len(self.tresorIdentifies) == len(tresorsImpossible):
            self.tresorIdentifies = []
        elif not tresorsImpossible:
            self.tresorIdentifies = np.delete(self.tresorIdentifies, tresorsImpossible)

    def getTresorsIdentifies(self):
        return self.tresorIdentifies
