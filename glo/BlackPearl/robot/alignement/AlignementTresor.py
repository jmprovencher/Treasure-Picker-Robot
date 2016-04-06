RATIOPIXEL_CM = 40


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

        return commande, distance

    def ajusterPositionY(self, distance_y):
        if (distance_y < 0):
            commande = 'backward'
        elif (distance_y > 0):
            commande = 'forward'

        distance = abs(distance_y / RATIOPIXEL_CM)+2
        return commande, distance
