import sys

sys.path.append('/home/design3/Desktop/design3/glo/BlackPearl')
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot
import time


def main():
    prefixPort = '/dev/tty.usbmodemFA131'
    monUART = UARTDriver(prefixPort, 115200)
    robot = Robot(monUART)
    robot.start()

    # for j in range(0, 20):
    #   try:
    #     port = prefixPort + str(j)
    #     monUART = UARTDriver(port, 115200)
    #     print('le bon port est: ' + port)
    #     robot = Robot(monUART)
    #     robot.start()
    #     break
    #   except Exception as e:
    #     print e
    #     print('mauvais port')

if __name__ == '__main__':
    main()
