import cv2
import numpy as np
from stationbase.vision.InfoTable import InfoTable
from stationbase.vision.Detection import Detection
from elements.Tresor import Tresor
LIMITE_INF_TABLE_1_Y = 45
LIMITE_SUP_TABLE_1_Y = 750
LIMITE_SUP_TABLE_1_X = 1342
LIMITE_INF_TABLE_2_Y = 45
LIMITE_SUP_TABLE_2_Y = 810
LIMITE_SUP_TABLE_2_X = 1350
LIMITE_INF_TABLE_3_Y = 90
LIMITE_SUP_TABLE_3_Y = 810
LIMITE_SUP_TABLE_3_X = 1327
LIMITE_INF_TABLE_5_Y = 50
LIMITE_SUP_TABLE_5_Y = 800
LIMITE_SUP_TABLE_5_X = 1350
LIMITE_INF_TABLE_6_Y = 100
LIMITE_SUP_TABLE_6_Y = 75
LIMITE_SUP_TABLE_6_X = 1345
MIN_AIRE_TRESOR = 30
MAX_AIRE_TRESOR = 300

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
        intervalleFonce, intervalleClair = InfoTable('Tresor', self.numeroTable).getIntervalle()
        masqueTresors = cv2.inRange(self.imageCamera, intervalleFonce, intervalleClair)
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(masqueTresors, cv2.MORPH_CLOSE, kernel)
        _, contoursTresors, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contoursTresors

    def eleminerCoutoursNegligeables(self, contoursTresors):
        contoursNegligeables = []

        for i in range(len(contoursTresors)):
            aire = cv2.contourArea(contoursTresors[i])
            if aire < MIN_AIRE_TRESOR or aire > MAX_AIRE_TRESOR:
                contoursNegligeables.append(i)

        if len(contoursTresors) == len(contoursNegligeables):
            contoursTresors = []
        elif contoursNegligeables:
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
                if (LIMITE_INF_TABLE_1_Y < y < LIMITE_SUP_TABLE_1_Y) or (x > LIMITE_SUP_TABLE_1_X):
                    tresorsImpossible.append(i)
            elif self.numeroTable == 2:
                if (LIMITE_INF_TABLE_2_Y < y < LIMITE_SUP_TABLE_2_Y) or (x > LIMITE_SUP_TABLE_2_X):
                    tresorsImpossible.append(i)
            elif self.numeroTable == 3:
                if (LIMITE_INF_TABLE_3_Y < y < LIMITE_SUP_TABLE_3_Y) or (x > LIMITE_SUP_TABLE_3_X):
                    tresorsImpossible.append(i)
            elif self.numeroTable == 5:
                if (LIMITE_INF_TABLE_5_Y < y < LIMITE_SUP_TABLE_5_Y) or (x > LIMITE_SUP_TABLE_5_X):
                    tresorsImpossible.append(i)
            elif self.numeroTable == 6:
                if (LIMITE_INF_TABLE_6_Y < y < LIMITE_SUP_TABLE_6_Y) or (x > LIMITE_SUP_TABLE_6_X):
                    tresorsImpossible.append(i)

        if len(self.tresorIdentifies) == len(tresorsImpossible):
            self.tresorIdentifies = []
        elif tresorsImpossible:
            self.tresorIdentifies = np.delete(self.tresorIdentifies, tresorsImpossible)

    def getTresorsIdentifies(self):
        return self.tresorIdentifies
