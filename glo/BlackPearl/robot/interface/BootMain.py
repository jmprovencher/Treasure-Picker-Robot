import sys
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot
sys.path.append('/home/design3/Desktop/design3/glo/BlackPearl')


def main():
    prefixPort = '/dev/ttyAMC'

    for j in range(0, 20):
      try:
        port = prefixPort + str(j)
        monUART = UARTDriver(port, 115200)
        print('le bon port est: ' + port)
        robot = Robot(monUART)
        robot.start()
        break
      except Exception as e:
        print e
        print('mauvais port')

if __name__ == '__main__':
    main()
