import socket
from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer
import  ConfigPath

verrou = RLock()

class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.monServeur = TCPServer()

    def run(self):
        self.attendreWakeUpRobot()
        while 1:
            if (self.stationBase.envoyerCommande):
                self.envoyerCommande()
            elif (self.stationBase.attenteDuRobot):
                data = self.attendreInfoRobot()
                self.traiterInfoRobot(data)
                time.sleep(20)
            else:
                time.sleep(20)

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
                print self.monServeur.connectionEstablished

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
                print 'connection etablie.'

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
                print 'connection etablie'

            if data == -1:
                print('Error while receiving file')



