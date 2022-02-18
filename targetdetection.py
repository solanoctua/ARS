import cv2 , time
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
prev_frame_time = 0
new_frame_time = 0
if cam.isOpened():
    ret,frame = cam.read()
else: 
    ret = False
while ret :
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    ret,frame = cam.read()
    frame_width, frame_height = (480,480)
    frame = cv2.resize(frame,(frame_width, frame_height))
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
    cv2.putText(red,"FPS:{}".format(int(fps)),(15,15),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1,cv2.LINE_AA)#Displays fps
    cv2.circle(red, (frame_width//2, frame_height//2), 25, (255,0,0), 1)
    contours, hierarchy = cv2.findContours(mask_red , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print("The number of red objects in the frame is {}".format(len(contours)-1))
    
    if len(contours) >= 1:
        # Sort all the contours wrt their areas to discard the small objects
        red_objects = sorted(contours, key=cv2.contourArea)
        red_objects = red_objects[-2:] # Take the 3 objects with the largest area
        for object in red_objects: 
            #print("Area = ",cv2.contourArea(object))
            if cv2.contourArea(object) >= 500: # If area is big enough, find its center etc.
                cv2.putText(red, "Red Object Detected", (35, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 255), 2)
                # Get the moments https://docs.opencv.org/3.4/d8/d23/classcv_1_1Moments.html
                moment = cv2.moments(object) # To find the center of the contour, we use cv2.moment
                center = (moment['m10'] / (moment['m00'] + 1e-5), moment['m01'] / (moment['m00'] + 1e-5)) # calculate center of the contour
                #print(center)
                color = (255, 255, 255)
                cv2.circle(red, (int(center[0]), int(center[1])), 15, color, -1) # draw circle at the center of the contour
                cv2.putText(red, "({},{})".format(int(center[0]) , int(center[1])), (int(center[0]) , int(center[1]) + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2) # write pixel coordinates
        
        result = cv2.drawContours(red, object, -1, (0,255,0), 3,lineType=cv2.FILLED) 
        cv2.imshow("result",result)
    
    """
    cv2.imshow("realTimeCameraH",H)
    cv2.imshow("realTimeCameraS",S)
    cv2.imshow("realTimeCameraV",V)
    cv2.imshow("realTimeCameraHSV",hsv_frame)
    """
    cv2.imshow("realTimeCameraRed",red)
    cv2.imshow("realTimeCamera",frame)
    
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
cam.release()   