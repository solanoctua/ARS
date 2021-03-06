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
    ret,frame = cam.read()
    frame_width, frame_height = (680,680)
    frame = cv2.resize(frame,(frame_width, frame_height))
    blank = np.zeros(frame.shape, np.uint8)
    #Calculate FPS
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame,"FPS:{}".format(int(fps)),(15,15),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1,cv2.LINE_AA)#Displays fps
    # lines for left,right,up,down boundaries
    target_lock_radius = 100
    cv2.circle(frame, (frame_width//2, frame_height//2), target_lock_radius, (255,0,0), 1)
    cv2.line(frame,(int(frame_width/2 +target_lock_radius),0),(int(frame_width/2 +target_lock_radius),int(frame_height)),(255,0,0),1)
    cv2.line(frame,(0,int(frame_height/2 + target_lock_radius)),(int(frame_width),int(frame_height/2 + target_lock_radius)),(255,0,0),1)
    cv2.line(frame,(int(frame_width/2 -target_lock_radius),0),(int(frame_width/2-target_lock_radius),int(frame_height)),(255,0,0),1)
    cv2.line(frame,(0,int(frame_height/2 - target_lock_radius)),(int(frame_width),int(frame_height/2 - target_lock_radius)),(255,0,0),1)
    # convert to HSV colorspace 
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
    
    contours, hierarchy = cv2.findContours(mask_red , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print("The number of red objects in the frame is {}".format(len(contours)-1))
    
    if len(contours) >= 1:

        # Sort all the contours wrt their areas to discard the small objects
        red_objects = sorted(contours, key=cv2.contourArea)
        red_objects = red_objects[-1:] # Take the object with the largest area
        for object in red_objects: 
            #print("Area = ",cv2.contourArea(object))
            if cv2.contourArea(object) >= 500: # If area is big enough, find its center etc.
                cv2.putText(frame, "Red Object Detected!", (35, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                # Get the moments https://docs.opencv.org/3.4/d8/d23/classcv_1_1Moments.html
                moment = cv2.moments(object) # To find the center of the contour, we use cv2.moment
                center = (moment['m10'] / (moment['m00'] + 1e-5), moment['m01'] / (moment['m00'] + 1e-5)) # calculate center of the contour
                print(center)
                color = (255, 255, 255)
                cv2.circle(frame, (int(center[0]), int(center[1])), 15, color, -1) # draw circle at the center of the contour
                cv2.putText(frame, "({},{})".format(int(center[0]) , int(center[1])), (int(center[0]) , int(center[1]) + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2) # write pixel coordinates
        
                cv2.drawContours(frame, object, -1, (0,255,0), 3, lineType=cv2.FILLED) 
                
                #draw a transparent rectangle to the zone, where our targeted object's center point lies.
                if(center[0] <= int(frame_width/2 -target_lock_radius) and center[1] <= int(frame_height/2 - target_lock_radius)):
                    #print("ZONE 1")
                    #To draw a rectangle, you need top-left corner and bottom-right corner of rectangle. 
                    cv2.rectangle(blank,(0,0),(int(frame_width/2 -target_lock_radius),int(frame_height/2 - target_lock_radius)),(0,255,0),cv2.FILLED)
                            
                elif(center[0] <= int(frame_width/2 -target_lock_radius) and center[1] >= int(frame_height/2 - target_lock_radius) and center[1] <= int(frame_height/2 + target_lock_radius)):
                    #print("ZONE 2")
                    cv2.rectangle(blank,(0,int(frame_height/2 - target_lock_radius)),(int(frame_width/2 -target_lock_radius),int(frame_height/2 + target_lock_radius)),(0,255,0),cv2.FILLED)
                elif(center[0] <= int(frame_width/2 -target_lock_radius) and center[1] >= int(frame_height/2 + target_lock_radius)):
                    #print("ZONE 3")
                    cv2.rectangle(blank,(0,int(frame_height/2 + target_lock_radius)),(int(frame_width/2 -target_lock_radius),int(frame_height)),(0,255,0),cv2.FILLED)
                elif(center[0] >= int(frame_width/2 -target_lock_radius) and center[0] <= int(frame_width/2 +target_lock_radius) and center[1] <= int(frame_height/2 - target_lock_radius)  ):
                    #print("ZONE 4")
                    cv2.rectangle(blank,(int(frame_width/2 -target_lock_radius),0),(int(frame_width/2 +target_lock_radius),int(frame_height/2 - target_lock_radius)),(0,255,0),cv2.FILLED)
                elif(center[0] >= int(frame_width/2 -target_lock_radius) and center[0] <= int(frame_width/2 +target_lock_radius) and center[1] >= int(frame_height/2 - target_lock_radius) and center[1] <= int(frame_height/2 + target_lock_radius)):
                    #print("ZONE 5")
                    cv2.rectangle(blank,(int(frame_width/2 -target_lock_radius),int(frame_height/2 - target_lock_radius)),(int(frame_width/2 + target_lock_radius),int(frame_height/2 + target_lock_radius)),(0,255,0),cv2.FILLED)
                elif(center[0] >= int(frame_width/2 -target_lock_radius) and center[0] <= int(frame_width/2 +target_lock_radius) and center[1] >= int(frame_height/2 + target_lock_radius)  ):
                    #print("ZONE 6")
                    cv2.rectangle(blank,(int(frame_width/2 -target_lock_radius),int(frame_height/2 + target_lock_radius)),(int(frame_width/2 +target_lock_radius),int(frame_height)),(0,255,0),cv2.FILLED)
                elif(center[0] >= int(frame_width/2 +target_lock_radius) and center[1] <= int(frame_height/2 - target_lock_radius)):
                    #print("ZONE 7")
                    cv2.rectangle(blank,(int(frame_width/2 +target_lock_radius),0),(int(frame_width),int(frame_height/2 - target_lock_radius)),(0,255,0),cv2.FILLED)
                elif(center[0] >= int(frame_width/2 +target_lock_radius) and center[1] >= int(frame_height/2 - target_lock_radius) and center[1] <= int(frame_height/2 + target_lock_radius)):
                    #print("ZONE 8")
                    cv2.rectangle(blank,(int(frame_width/2 +target_lock_radius),int(frame_height/2 - target_lock_radius)),(int(frame_width),int(frame_height/2 + target_lock_radius)),(0,255,0),cv2.FILLED)
                elif(center[0] >= int(frame_width/2 +target_lock_radius) and center[1] >= int(frame_height/2 + target_lock_radius)):
                    #print("ZONE 9")
                    cv2.rectangle(blank,(int(frame_width/2 +target_lock_radius),int(frame_height/2 + target_lock_radius)),(int(frame_width),int(frame_height)),(0,255,0),cv2.FILLED)
                else:
                    pass        
                alpha = 0.4
                beta = (1.0 - alpha)
                cv2.addWeighted(blank, alpha, frame, beta, 0.0,frame) # to make rectangle transparent
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
