import cv2
import numpy as np

def nothing(x):
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("min - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("min - S", "Trackbars", 84, 255, nothing)
cv2.createTrackbar("min - V", "Trackbars", 148, 255, nothing)
cv2.createTrackbar("max - H", "Trackbars", 6, 179, nothing)
cv2.createTrackbar("max - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("max - V", "Trackbars", 255, 255, nothing)
cam = cv2.VideoCapture(0)
if cam.isOpened():
    ret,frame = cam.read()
else: 
    ret = False
while ret :
    ret,frame = cam.read()
    frame = cv2.resize(frame,(480,480))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(hsv_frame)
    #Red Color
    """
    min_red = np.array([0,70,50])
    max_red = np.array([10,255,255])
    """
    min_h = cv2.getTrackbarPos("min - H", "Trackbars")
    min_s = cv2.getTrackbarPos("min - S", "Trackbars")
    min_v = cv2.getTrackbarPos("min - V", "Trackbars")
    max_h = cv2.getTrackbarPos("max - H", "Trackbars")
    max_s = cv2.getTrackbarPos("max - S", "Trackbars")
    max_v = cv2.getTrackbarPos("max - V", "Trackbars")
    min_red = np.array([min_h, min_s, min_v])
    max_red = np.array([max_h, max_s, max_v])
    
    
    mask_red = cv2.inRange(hsv_frame, min_red, max_red)
    red = cv2.bitwise_and(frame, frame, mask = mask_red)
   
    cv2.imshow("realTimeCameraRed",red)
    """
    cv2.imshow("realTimeCameraH",H)
    cv2.imshow("realTimeCameraS",S)
    cv2.imshow("realTimeCameraV",V)
    cv2.imshow("realTimeCameraHSV",hsv_frame)
    """
    cv2.imshow("realTimeCamera",frame)
    
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
cam.release()   