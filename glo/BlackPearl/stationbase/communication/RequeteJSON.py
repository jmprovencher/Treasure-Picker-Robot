import json
import ConfigPath


class RequeteJSON():
    def __init__(self, commande, parametre):
        self.commande = commande
        self.parametre = parametre
        self.data = self._definirRequete(self.commande, self.parametre)

    def _definirRequete(self, commande, parametre):
        self.data = {
            'commande': commande,
            'parametre': parametre,
        }
        return self.data


