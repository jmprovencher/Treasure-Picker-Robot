from UARTDriver import UARTDriver
from TCPClient import TCPClient
from threading import Thread, RLock
import time
from robot.communication.RequeteJSON import RequeteJSON

verrou = RLock()


class RobotClient(Thread):
    def __init__(self, robot, adresseIP):
        Thread.__init__(self)
        self.robot = robot
        self.adresseIP = adresseIP
        self.termineeAEteEnvoyerAStation = True
        self.demarrageTermine = False
        self.monClient = TCPClient(self.adresseIP)

    def run(self):
        self.monClient._connectToServer()
        while not self.demarrageTermine:
            time.sleep(1)
            print("Attends demarrage...")
        print("Demarrage est terminee, envoie pret a station")
        self.envoyerPretAStation()
        data = self.attendreCommande()
        self.traiterCommande(data)
        while 1:
            print("Thread client....")
            if self.robot.pretEnvoyerLettre:
                print("Envoie de la lettre...")
                self.envoyerLettre()
                self.robot.indiceObtenu = self.robot.service.obtenirCible(self.robot.lettreObtenue)
                print(self.robot.indiceObtenu)
                self.envoyerIndice()
                self.robot.pretEnvoyerLettre = False
            if self.robot.commandeTerminee and not self.robot.alignementEnCours:
                    self.envoyerTension()
                    self.envoyerCommandeTerminee()
                    data = self.attendreCommande()
                    self.traiterCommande(data)
            else:
                print("Else envoie tension")
                self.envoyerTension()

    def attendreCommande(self):
        data = -1
        while 1:
            try:
                data = self.monClient.receiveFile()
                break
            except Exception as e:
                print e
                print "Connection perdue... Tente de reconnecter..."
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()
        if data == -1:
            print("Erreur lors de la lecture du fichier")

        self.termineeAEteEnvoyerAStation = False
        return data

    def traiterCommande(self, data):
        print data
        commande = data['commande']
        parametre = data['parametre']
        self.robot.traiterCommande(commande, parametre)
        self.termineeAEteEnvoyerAStation = False

    def envoyerTension(self):
        RequeteJSON("tension", self.robot.tensionCondensateur)
        while 1:
            try:
                self.monClient.sendFile()
                break
            except Exception as e:
                print e
                print "Connection perdue... Tente de reconnecter..."
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()

    def envoyerLettre(self):
        RequeteJSON("man: " + self.robot.lettreObtenue, 0)
        while 1:
            try:
                self.monClient.sendFile()
                self.robot.pretEnvoyerLettre = False
                break
            except Exception as e:
                print e
                print "Connection perdue... Tente de reconnecter..."
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()

    def envoyerIndice(self):
        RequeteJSON("indice: " + self.robot.indiceObtenu, 0)
        while 1:
            try:
                self.monClient.sendFile()
                self.robot.pretEnvoyerIndice = False
                break
            except Exception as e:
                print e
                print "Connection perdue... Tente de reconnecter..."
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()

    def envoyerCommandeTerminee(self):
        RequeteJSON("termine", 0)
        while 1:
            try:
                self.monClient.sendFile()
                break
            except Exception as e:
                print e
                print "Connection perdue... Tente de reconnecter..."
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()
        self.robot.commandeTerminee = False
        self.termineeAEteEnvoyerAStation = True

    def envoyerPretAStation(self):
        RequeteJSON("robotPret", 0)
        while 1:
            try:
                self.monClient.sendFile()
                break
            except Exception as e:
                print e
                print "Connection perdue... Tente de reconnecter..."
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()
            time.sleep(0.1)
