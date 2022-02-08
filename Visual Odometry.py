import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
from ADMS import * # Adaptive Non Maximal Suppresion for homogeneous spatial keypoint distribution

# Horizontal stereo: the first and the second camera views are shifted relative to each other mainly along the x-axis (with possible small vertical shift).
# In the rectified images, the corresponding epipolar lines in the left and right cameras are horizontal and have the same y-coordinate.

camMtx_left =np.array( [ [1  , 0. , 1  ], 
                         [0. , 1  , 1  ],
                         [0. , 0. , 1. ] ])

camMTX_right =np.array( [ [1  , 0. , 1  ], 
                          [0. , 1  , 1  ],
                          [0. , 0. , 1. ] ])

cam_left = cv2.VideoCapture(0)
cam_right = cv2.VideoCapture(1)

if cam_left.isOpened() and cam_right.isOpened() :
    ret_left , frame_left = self.cam_left.read()
    ret_right , frame_right = self.cam_right.read()     
 else:
    ret1,ret2 = False

while ret1 and ret2:
    ret_left , frame_left = self.cam_left.read()
    ret_right , frame_right = self.cam_right.read()

    #CONSIDER HSV FILTER HERE


    # Downscale for faster processing
    downScale = 0.5
    [frame_left, frame_right]= scale_images(frame_left, frame_right, downScale)
    frameSize = frame_left.shape[:2][::-1]

    # Undistort and rectify 
    mapL1, mapL2 = cv2.fisheye.initUndistortRectifyMap(leftCamMtx, leftCamDist, np.eye(3), mtx, size=frameSize, m1type= cv2.CV_16SC2)  #cv2.CV_16SC2
    undistorted_left = cv2.remap(frame_left, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT )
    mapR1, mapR2 = cv2.fisheye.initUndistortRectifyMap(rightCamMtx, leftCamDist, np.eye(3), mtx, size=frameSize, m1type= cv2.CV_16SC2)  #cv2.CV_16SC2
    undistorted_right = cv2.remap(frame_right, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT )

    stereo = cv2.StereoSGBM_create(	[, minDisparity[, numDisparities[, blockSize[, P1[, P2[, disp12MaxDiff[, preFilterCap[, uniquenessRatio[, speckleWindowSize[, speckleRange[, mode]]]]]]]]]]]
    disparity_map = stereo.compute(undistorted_left, undistorted_right)

    # Feature Detection/Matching
    fast = cv2.FastFeatureDetector_create()
        keypoints = fast.detect(img, None)
        img2 = cv2.drawKeypoints(img, keypoints, outImage=None, color=(255, 0, 0))
        cv2.imshow("Detected FAST keypoints", img2)
        cv2.waitKey(0)

        # keypoints should be sorted by strength in descending order
        # before feeding to SSC to work correctly
        keypoints = sorted(keypoints, key=lambda x: x.response, reverse=True)

        selected_keypoints = ssc( keypoints, args.num_ret_points, args.tolerance, img.shape[1], img.shape[0])

        img3 = cv2.drawKeypoints(img, selected_keypoints, outImage=None, color=(255, 0, 0))
        cv2.imshow("Selected keypoints", img3)

    # Motion Estimation

    if cv2.waitKey(1) == 27:   #press esc to quit
        self.cap.release()
        cv2.destroyAllWindows()
        break