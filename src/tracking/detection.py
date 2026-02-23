import cv2 as cv
import cv2.aruco as aruco
import sys
import os
import numpy as np

sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))

from tools.read_config_file import get_num_camera


#initilizing video_image
num_camera = get_num_camera()
cap = cv.VideoCapture(num_camera) #change if it is neccesary 


#choose dictionary
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)


# function for detector parameters
detectorParams = aruco.DetectorParameters()

#making detector
detector = aruco.ArucoDetector(dictionary, detectorParams)

#infinite bucle 
while True:
    ret, frame = cap.read()
    if not ret : continue

    #detect markers

    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    print(markerIds)
    output_frame = frame.copy()
    aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

    cv.imshow("Detected ArUco", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    

cv.destroyAllWindows()