from tkinter import Frame
import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if cam.isOpened():
    ret,frame = cam.read()
else: 
    ret = False
while ret :
    ret,frame = cam.read()
    cv2.imshow("realTimeCamera",frame)
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
cam.release()   