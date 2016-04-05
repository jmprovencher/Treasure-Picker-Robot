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

        distance_cm = math.floor(abs(distance_x))
        distance_mm = int(math.floor((abs(distance_x) - distance_cm) * 10))

        if (distance_mm >= 1):
            self._ajusterPositionLaterale_MM(commande, distance_mm)

        return commande, int(distance_cm)

    def _ajusterPositionLaterale_MM(self, commande, distance_mm):
        if (distance_mm > 0):
            commande = commande + 'P'
        elif (distance_mm < 0):
            commande = commande + 'P'

        distance = abs(round(distance_mm))

        self.ajustements.append((commande, distance))
        print(commande, int(distance))


    def _ajusterPositionY(self, distance_y):
        if (distance_y < 0):
            commande = 'backward'
        elif (distance_y > 0):
            commande = 'forward'

        distance_cm = math.ceil(abs(distance_y)) + 1


        return commande, int(distance_cm)