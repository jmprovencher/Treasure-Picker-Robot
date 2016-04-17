from threading import Thread, RLock

verrou = RLock()
INFO_DONE = 'done'
QUATRE_LETTRE_MANCHESTER = 4


class LectureUART(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot

    def run(self):
        while 1:
            info = self.robot.uartDriver.UART.read(4)
            self.analyserLecture(info)

    def analyserLecture(self, info):
        print("UART READ: %s" % info)
        lettre_manchester = info[0]
        if info == INFO_DONE:
            self.robot.commandeTerminee = True
        elif info.count(lettre_manchester) == QUATRE_LETTRE_MANCHESTER:
            self.robot.lettreObtenue = lettre_manchester
            print(self.robot.lettreObtenue)
            print("robot pret a envoyer lettre")
        else:
            self.robot.tensionCondensateur = info
