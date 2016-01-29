import cv2
import numpy as np

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print x,y
        print img[x,y]
# Create a black image, a window and bind the function to window
#img = cv2.imread('Table3/2016-01-24-154511.jpg')
img = cv2.imread('noir.png')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

#set mouse callback function for window
cv2.setMouseCallback('image', mouse_callback)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF

cv2.destroyAllWindows()