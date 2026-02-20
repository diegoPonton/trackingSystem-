import cv2
import numpy as np


## DICCIONARIO DE MARCADORES 

dict = cv2.aruco.Dictionary(cv2.aruco.DICT_6X6_100)


## ID MARCADOR

marker_id = 42
marker_size = 200

marker_image = cv2.aruco.generateImageMarker(dict, marker_id, marker_size)





## MOSTRAR MARCADOR 
cv2.imwrite("marker_42.png", marker_image)
cv2.imshow("ArUco Marker", marker_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
