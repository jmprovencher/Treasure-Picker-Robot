import sys
sys.path.append('/home/design3/Desktop/design3/glo/BlackPearl')
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot


def main():
    prefixPort = '/dev/ttyAMC'
    # monUART = None
    # robot = Robot(monUART)
    # robot.start()

    prefixPort = '/dev/ttyACM'

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
