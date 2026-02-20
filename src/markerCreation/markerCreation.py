import cv2 as cv
import matplotlib.pyplot as plt

## SELECCIONAR DICCIONARIO DE MARCADORES 

dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)


## SETEAR PARAMETROS DE DETECCION

markerId = 0
markerSize = 200 ## TAMAÑO DEL MARCADOR EN PIXELES

marker = cv.aruco.generateImageMarker(dict, markerId, markerSize)


## MOSTRAR MARCADOR 

plt.imshow(marker, cmap="gray")
plt.show()



