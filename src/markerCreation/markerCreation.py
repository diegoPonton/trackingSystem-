import sys
import os
sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))

import cv2 as cv
import matplotlib.pyplot as plt

from tools.read_config_file import get_route_aruco


route_arauco = get_route_aruco()


## SELECCIONAR DICCIONARIO DE MARCADORES 

dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)


## SETEAR PARAMETROS DE DETECCION

markerId = 0
markerSize = 250 ## TAMAÑO DEL MARCADOR EN PIXELES
num_images_generated = 20

for id in range(num_images_generated):
    marker = cv.aruco.generateImageMarker(dict, id, markerSize)
    cv.imwrite(os.path.join(route_arauco, ("code_arauco_" + str(id) + ".jpg")), marker)

## MOSTRAR MARCADOR 

#plt.imshow(marker, cmap="gray")
#plt.show()


#generating differents aRuco and save it



