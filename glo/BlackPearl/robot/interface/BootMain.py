import sys
sys.path.append('/home/design3/Desktop/design3/glo/BlackPearl')
from robot.communication.UARTDriver import UARTDriver
from robot.interface.Robot import Robot
import time

def main():
	listePorts = '/dev/ttyACM'
	for j in range(0, 20):
	    try:
                maVariable = listePorts + str(j)
    	        monUART = UARTDriver(maVariable, 115200) #on linux
    	        #monUART = None
    	        robot = Robot(monUART)
		print('le bon port est: ')
		print(j)
	        break
	    except:
	        print('mauvais port')
	robot.start()

if __name__ == '__main__':
    main()
