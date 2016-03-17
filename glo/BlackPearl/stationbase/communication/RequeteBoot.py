import json

#CLASS STATUS
# Pas implementer encore

class RequeteBoot():
    def __init__(self, commande, status):
        # Status serait un bool de checkup pour un test de systeme complet avant le demarrage

        self.commande = commande
        self.status = status
        self.data = self._definirRequete(self.commande, self.status)
        self._serialiser()

    def _definirRequete(self, commande, parametre):
        self.data = {
            'communication': commande,
            'parametre': parametre,
        }
        return self.data

    def _serialiser(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f)
