from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer
from elements.Cible import Cible

COMMANDE_TENSION = "tension"
COMMANDE_ROBOT_PRET = "robotPret"
COMMANDE_INDICE = "indice "
COMMANDE_MAN = "man "
COMMANDE_TERMINE = "termine"
COMMANDE_PRESENT = 'present'
COMMANDE_ABSENT = 'absent'


class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.pretEnvoyerCommande = False
        self.robotEstPret = False
        self.tresorTrouve = False
        self.attenteDuRobot = False
        self.monServeur = TCPServer()

    def run(self):
        self.monServeur.connection = self.monServeur.establishConnection()
        self.attendreWakeUpRobot()
        while 1:
            if self.pretEnvoyerCommande:
                self.envoyerCommande()
            elif self.attenteDuRobot:
                data = self.attendreInfoRobot()
                self.traiterInfoRobot(data)
                time.sleep(0.5)
            else:
                time.sleep(0.5)

    def envoyerCommande(self):
        while 1:
            try:
                self.monServeur.sendFile()
                self.pretEnvoyerCommande = False
                break
            except Exception as e:
                print e
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur.establishConnection()
                print 'Connection retablite'

    def attendreInfoRobot(self):
        print '\nAttente du robot...'
        while self.attenteDuRobot:
            try:
                data = self.monServeur.receiveFile()
                break
            except Exception as e:
                print e
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur.establishConnection()
                print 'connection retablite.'
        return data

    def traiterInfoRobot(self, data):
        commande = data['commande']
        parametre = data['parametre']
        if commande == COMMANDE_TENSION:
            self.stationBase.setTensionCondensateur(parametre)
            print "Tension: %s" % parametre
        elif commande == COMMANDE_ROBOT_PRET:
            self.robotEstPret = True
            print "Le robot est pret."
        elif commande.startswith(COMMANDE_INDICE):
            indice = commande[7:]
            print ("L'indice: %s" % indice)
            self.stationBase.carte.setCible(Cible([self.stationBase.carte, indice]))
        elif commande.startswith(COMMANDE_MAN):
            self.stationBase.manchester = commande[-1]
            print ("Code manchester: %s" % self.stationBase.getManchester())
        elif commande == COMMANDE_TERMINE:
            print 'Commande termine.'
            self.attenteDuRobot = False
        elif commande == COMMANDE_PRESENT:
            self.tresorTrouve = True
            self.attenteDuRobot = False
        elif commande == COMMANDE_ABSENT:
            self.attenteDuRobot = False

    def attendreWakeUpRobot(self):
        while 1:
            try:
                data = self.monServeur.receiveFile()
                commande = data['commande']
                if commande == COMMANDE_ROBOT_PRET:
                    self.robotEstPret = True
                    break
            except Exception as e:
                print e
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur.establishConnection()
                print 'connection retablite'

    def getRobotPret(self):
        return self.robotEstPret

    def signalerEnvoyerCommande(self):
        self.pretEnvoyerCommande = True

    def debuteAttenteDuRobot(self):
        self.attenteDuRobot = True

    def getAttenteDuRobot(self):
        return self.attenteDuRobot




