import math


class AlignementStation():
    def __init__(self):
        self.terminer = False
        self.ajustements = []

    def calculerAjustement(self, distance_x, distance_y):
        ajustements_x = self._ajusterPositionLaterale_CM(distance_x)
        if (ajustements_x[1] >= 1):
            self.ajustements.append(ajustements_x)

        ajustements_y = self._ajusterPositionY(distance_y)
        self.ajustements.append(ajustements_y)

        return self.ajustements

    def _ajusterPositionLaterale_CM(self, distance_x):
        if (distance_x > 0):
            commande = 'left'
        elif (distance_x < 0):
            commande = 'right'
        distance_x = abs(distance_x)
        #distance_cm = math.floor(abs(distance_x))
        distance_cm = int(math.floor(distance_x))
        #ajustement_cm = int(round(distance_x,0))
        distance_mm = int(math.floor((abs(distance_x) - distance_cm) * 10))
        #print("Distance mm a bouger: %d" % distance_mm)


        if (distance_mm > 2) and distance_cm <=1:
            self._ajusterPositionLaterale_MM(commande, distance_mm)
            return commande, distance_cm
        elif distance_cm <= 2:
            return commande, int(round(distance_x, 0))
        else:
            return commande, int(math.floor(distance_x))


    def _ajusterPositionLaterale_MM(self, commande, distance_mm):

        commande = commande + 'P'
        distance = abs(round(distance_mm))

        self.ajustements.append((commande, distance))
        print(commande, int(distance))

    def _ajusterPositionY(self, distance_y):
        if (distance_y < 0):
            commande = 'backward'
        elif (distance_y > 0):
            commande = 'forward'

        distance_cm = int(round(abs(distance_y), 0))

        return commande, int(distance_cm)
