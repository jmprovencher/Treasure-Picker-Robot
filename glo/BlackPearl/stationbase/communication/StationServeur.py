from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer
from elements.Cible import Cible


class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.monServeur = TCPServer()

    def run(self):
        self.monServeur.connection = self.monServeur.establishConnection()
        self.attendreWakeUpRobot()
        while 1:
            if self.stationBase.envoyerCommande:
                self.envoyerCommande()
            elif self.stationBase.attenteDuRobot:
                data = self.attendreInfoRobot()
                self.traiterInfoRobot(data)
                time.sleep(0.01)
            else:
                time.sleep(0.01)

    def envoyerCommande(self):
        while 1:
            try:
                self.monServeur.sendFile()
                self.stationBase.envoyerCommande = False
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
        while self.stationBase.attenteDuRobot:
            try:
                data = self.monServeur.receiveFile()
                self.traiterInfoRobot(data)
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
        if commande == "tension":
            self.stationBase.setTensionCondensateur(parametre)
            print "Tension: %s" % parametre
        elif commande == "robotPret":
            self.stationBase.robotEstPret = True
            print "Le robot est pret."
        elif commande.startswith("indice: "):
            indice = commande[8:]
            print ("L'indice: %s" % indice)
            self.stationBase.getCarte().setCible(Cible(self.stationBase.carte, indice))
        elif commande.startswith("man: "):
            self.stationBase.manchester = commande[-1]
            print ("Code manchester: %s" % self.stationBase.getManchester())
        elif commande == "termine":
            print 'Commande termine.'
            self.stationBase.attenteDuRobot = False

    def attendreWakeUpRobot(self):
        while 1:
            try:
                data = self.monServeur.receiveFile()
                commande = data['commande']
                if commande == "robotPret":
                    self.stationBase.robotEstPret = True
                    break
            except Exception as e:
                print e
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur.establishConnection()
                print 'connection retablite'





