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
        self.monClient = TCPClient(self.adresseIP)

    def run(self):
        self.monClient._connectToServer()
        while not (self.robot.tacheTerminee):
            print("Robot Client running")
            self.envoyerPretAStation()
            while 1:
                if (self.robot.pretEnvoyerLettre):
                    self.envoyerLettre()
                if (self.robot.pretEnvoyerIndice):
                    self.envoyerIndice()
                if (self.termineeAEteEnvoyerAStation):
                    data = self.attendreCommande()
                    self.traiterCommande(data)
                else:
                    if (self.robot.commandeTerminee) and not self.robot.alignementEnCours:
                        self.envoyerTension()
                        self.envoyerCommandeTerminee()
                        time.sleep(0.5)

    def attendreCommande(self):
        data = -1
        while 1:
            try:
                data = self.monClient.receiveFile()
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()
        if data == -1:
            print('Error while receiving file')

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
                print "Connection Lost, Trying to reconnect"
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
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()

    def envoyerIndice(self):
        RequeteJSON("cible: " + self.robot.indiceObtenu, 0)
        while 1:
            try:
                self.monClient.sendFile()
                self.robot.pretEnvoyerIndice = False
                break
            except Exception as e:
                print e
                print "Connection Lost, Trying to reconnect"
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
                print "Connection Lost, Trying to reconnect"
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
                print "Connection Lost, Trying to reconnect"
                time.sleep(0.1)
                self.monClient = TCPClient(self.adresseIP)
                self.monClient._connectToServer()
            time.sleep(0.1)
