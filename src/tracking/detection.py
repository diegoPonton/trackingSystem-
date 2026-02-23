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


##examlpe
point = []

#infinite bucle 




ret, frame = cap.read()
trail = np.zeros_like(frame)

previous_center = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Detectar marcadores
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

    if markerIds is not None and markerIds.size > 0 and markerIds[0] == 1:
        points = markerCorners[0][0]

        # Centro usando numpy (más limpio)
        center = tuple(np.mean(points, axis=0).astype(int))

        # Dibujar línea desde punto anterior
        if previous_center is not None:
            cv.line(trail, previous_center, center, (0, 255, 125), 2)

        previous_center = center

        # Dibujar punto actual
        cv.circle(frame, center, 6, (0, 125, 255), -1)

    # Combinar frame actual + trayectoria
    output = cv.add(frame, trail)

    cv.imshow("Detected ArUco", output)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()