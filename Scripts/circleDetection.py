import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if cam.isOpened():
    ret,frame = cam.read()
else: 
    ret = False
while ret :
    
    ret,frame = cam.read()
    frame_width, frame_height = (200,200)
    #frame = cv2.resize(frame,(frame_width, frame_height))
    # Convert to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                param2 = 50, minRadius = 50, maxRadius = 1000)
    
    # Draw circles that are detected.
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        print(detected_circles)
        
        for circle in detected_circles[0, :]:
            x, y, r = circle
    
            # Draw the circumference of the circle.
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
    
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(frame, (x, y), 5, (0, 0, 255), 3)
    cv2.imshow("Detected Circle", frame)
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
cam.release()
    
