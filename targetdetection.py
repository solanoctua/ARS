
import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if cam.isOpened():
    ret,frame = cam.read()
else: 
    ret = False
while ret :
    ret,frame = cam.read()
    frame = cv2.resize(frame,(360,360))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(hsv_frame)
    #Red Color
    min_red = np.array([0,70,50])
    max_red = np.array([10,255,255])
    
    mask_red = cv2.inRange(hsv_frame, min_red, max_red)
    red = cv2.bitwise_and(frame, frame, mask = mask_red)
   
    cv2.imshow("realTimeCameraRed",red)
    """
    cv2.imshow("realTimeCameraH",H)
    cv2.imshow("realTimeCameraS",S)
    cv2.imshow("realTimeCameraV",V)
    cv2.imshow("realTimeCamera",frame)
    """
    cv2.imshow("realTimeCameraHSV",hsv_frame)
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
cam.release()   