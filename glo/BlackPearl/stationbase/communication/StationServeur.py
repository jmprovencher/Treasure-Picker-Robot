import socket
from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer
from elements.Cible import Cible

verrou = RLock()

class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.monServeur = TCPServer()

    def run(self):
        self.monServeur.connection = self.monServeur._establishConnection()
        self.attendreWakeUpRobot()
        while 1:
            if (self.stationBase.envoyerCommande):
                self.envoyerCommande()
            elif (self.stationBase.attenteDuRobot):
                data = self.attendreInfoRobot()
                self.traiterInfoRobot(data)
                print("Station lecture fichier")
                time.sleep(1)
            else:
                time.sleep(1)

    def envoyerCommande(self):
        while 1:
            try:
                self.monServeur.sendFile()
                self.stationBase.envoyerCommande = False
                break
            except:
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur._establishConnection()
                print 'Connection retablite'

    def attendreInfoRobot(self):
        print '\nAttente du robot...'
        data = -1
        while self.stationBase.attenteDuRobot:
            try:
                data = self.monServeur.receiveFile()
                self.traiterInfoRobot(data)
            except Exception as e:
                print e
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur._establishConnection()
                print 'connection retablite.'

            if data == -1:
                print('Error while receiving file')

            return data

    def traiterInfoRobot(self, data):
        print data
        commande = data['commande']
        parametre = data['parametre']
        if (commande == "tension"):
            self.stationBase.tensionCondensateur = parametre
        elif (commande == "robotPret"):
            self.stationBase.robotEstPret = True
        elif (commande.startswith("cible: ")):
             print("COMMANDE:",commande)
             indice = commande[7:]
             print("Indice recu par la station %s" % indice)
             self.stationBase.carte.cible = Cible(self.stationBase.carte, indice)
        elif (commande.startswith("man: ")):
            self.stationBase.manchester = commande[-1]
            print("Code manchester recu par la station %s" % self.stationBase.manchester)
        elif (commande == "termine"):
            print 'commande termine recu et traite'
            self.stationBase.attenteDuRobot = False

    def attendreWakeUpRobot(self):
        data = -1
        while 1:
            try:
                data = self.monServeur.receiveFile()
                commande = data['commande']
                if (commande == "robotPret"):
                    self.stationBase.robotEstPret = True
                    break
            except Exception as e:
                print e
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                self.monServeur.connection = self.monServeur._establishConnection()
                print 'connection retablite'

            if data == -1:
                print('Error while receiving file')



