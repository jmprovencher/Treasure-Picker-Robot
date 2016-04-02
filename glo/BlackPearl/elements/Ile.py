from elements.ElementCartographique import ElementCartographique


class Ile(ElementCartographique):
    def __init__(self, centre, couleur, forme):
        ElementCartographique.__init__(self, centre)
        self.couleur = couleur
        self.forme = forme

    def getCouleur(self):
        return self.couleur

    def getForme(self):
        return self.forme
