import cv2
import numpy as np
def nothing(x):
    # any operation
    pass
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("min - H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("min - S", "Trackbars", 68, 255, nothing)
cv2.createTrackbar("min - V", "Trackbars", 154, 255, nothing)
cv2.createTrackbar("max - H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("max - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("max - V", "Trackbars", 243, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX
if cap.isOpened():
    ret,frame = cap.read()
else: 
    ret = False
while ret :
    ret, frame = cap.read()
    frame_width, frame_height = (480,480)
    frame = cv2.resize(frame,(frame_width, frame_height))
    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("min - H", "Trackbars")
    l_s = cv2.getTrackbarPos("min - S", "Trackbars")
    l_v = cv2.getTrackbarPos("min - V", "Trackbars")
    u_h = cv2.getTrackbarPos("max - H", "Trackbars")
    u_s = cv2.getTrackbarPos("max - S", "Trackbars")
    u_v = cv2.getTrackbarPos("max - V", "Trackbars")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        x= approx.ravel()[0]
        y= approx.ravel()[1]
    
        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            if len(approx) == 3:
                cv2.putText(frame, "Triangle", (x,y), font, 1, (0, 0, 0))
            elif len(approx) == 4:
                cv2.putText(frame, "Rectangle", (x,y), font, 1, (0, 0, 0))
            elif 10 < len(approx) < 20:
                cv2.putText(frame, "Circle", (x,y), font, 1, (0, 0, 0))
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
cap.release()   
