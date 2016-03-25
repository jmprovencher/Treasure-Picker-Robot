import json

class RequeteJSON():
    def __init__(self, commande, parametre):
        self.commande = commande
        self.parametre = parametre
        self.data = self._definirRequete(self.commande, self.parametre)
        self._serialiser()

    def _definirRequete(self, commande, parametre):
        self.data = {
            'commande': commande,
            'parametre': parametre,
        }
        return self.data

    def _serialiser(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f)
