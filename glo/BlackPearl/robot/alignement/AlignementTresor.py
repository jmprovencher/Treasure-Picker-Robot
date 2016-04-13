RATIOPIXEL_CM = 40
import math


class AlignementTresor():
    def __init__(self):
        self.terminer = False
        self.ajustements = []

    def calculerAjustement(self, distance_x, distance_y):
        if (abs(distance_x) > RATIOPIXEL_CM):
            ajustements_x = self.ajusterPositionX(distance_x)
            print(ajustements_x)
            self.ajustements.append(ajustements_x)
        if (abs(distance_y) > RATIOPIXEL_CM):
            ajustements_y = self.ajusterPositionY(distance_y)
            print(ajustements_y)
            self.ajustements.append(ajustements_y)
        return self.ajustements

    def ajusterPositionX(self, distance_x):
        if (distance_x < 0):
            commande = 'left'
        elif (distance_x > 0):
            commande = 'right'

        distance = abs(distance_x / RATIOPIXEL_CM)

        distance_cm = math.floor((distance))
        # ajustement_cm = int(round(distance_x,0))
        distance_mm = int(math.floor((abs(distance) - distance_cm) * 10))
        # print("Distance mm a bouger: %d" % distance_mm)

        if (distance_x >= 1):
            return commande, distance_cm
        elif (distance_mm > 3) and (distance_x < 1):
            self._ajusterPositionLaterale_MM(commande, distance_mm)
            
        return commande, distance_cm

        return commande, distance

    def _ajusterPositionLaterale_MM(self, commande, distance_mm):

        commande = commande + 'P'
        distance = abs(round(distance_mm))

        self.ajustements.append((commande, distance))
        print(commande, int(distance))

    def ajusterPositionY(self, distance_y):
        if (distance_y < 0):
            commande = 'backward'
        elif (distance_y > 0):
            commande = 'forward'

        distance = abs(distance_y / RATIOPIXEL_CM)+1
        if (distance_y < 5):
            self.ajustements.append(('backward', 5))
            distance = distance + 4
        return commande, abs(distance)
