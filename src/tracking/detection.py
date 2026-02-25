import cv2 as cv
import cv2.aruco as aruco
import sys
import os
import numpy as np
from writingDetectionOnCSV import append_positions_to_csv

sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))
from tools.read_config_file import get_num_camera, get_route_center_positions



num_camera = get_num_camera()
routeCSV = get_route_center_positions()

cap = cv.VideoCapture(num_camera)

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
detectorParams = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, detectorParams)

ret, frame = cap.read()
if not ret:
    raise RuntimeError("No se pudo leer de la cámara")

trail = np.zeros_like(frame)
previous_centers = {}  # {id: [(x,y), (x,y), ...]}
ids = []

# imprimir 1 vez por segundo
last_print = cv.getTickCount()
freq = cv.getTickFrequency()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    markerCorners, markerIds, _ = detector.detectMarkers(frame)

    if markerIds is not None and markerIds.size > 0:
        ids = markerIds.flatten()

        aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

        for i, mid in enumerate(ids):
            mid = int(mid)

            points = markerCorners[i][0]
            cx, cy = points.mean(axis=0)
            center = (int(cx), int(cy))

            if mid not in previous_centers:
                previous_centers[mid] = []

            previous_centers[mid].append(center)

            if len(previous_centers[mid]) >= 2:
                p1 = previous_centers[mid][-2]
                p2 = previous_centers[mid][-1]
                cv.line(trail, p1, p2, (0, 255, 125), 2)

            cv.circle(frame, center, 6, (0, 125, 255), -1)
            cv.putText(frame, f"ID {mid}", (center[0] + 8, center[1] - 8),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # print SOLO 1 vez por segundo (no por frame)
        now = cv.getTickCount()
        if (now - last_print) / freq >= 1.0:
            print("posiciones actuales:", {int(mid): previous_centers[int(mid)][-1] for mid in ids})
            last_print = now

    output = cv.add(frame, trail)
    cv.imshow("Detected ArUco", output)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        trail[:] = 0  # limpiar trayectoria

# ---- ESCRIBIR POSICIONES (última posición por ID) ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(BASE_DIR, routeCSV)
os.makedirs(out_dir, exist_ok=True)

csv_path = os.path.join(out_dir, "positions.csv")
append_positions_to_csv(previous_centers, csv_path)   

cap.release()
cv.destroyAllWindows()
print("CSV guardado en:", csv_path)