import cv2 as cv
import numpy as np
from time import sleep

#for import files, change when the project is finilized to contruct modules
import sys
import os
sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))


from tools.read_config_file import making_routes, get_route_figcal, get_num_camera

making_routes()
destination = get_route_figcal()
num_camera = get_num_camera()

cap = cv.VideoCapture(num_camera) #change if it is neccesary 


    


def take_pics(num_pics = 30):
    print(destination)
    cont_pic = 0

    print("##### Tomando fotos para la calibracion")
    pics = []
    while cont_pic < num_pics:
        ret, frame = cap.read()  
        if ret: 
            pics.append(frame) 
        else: 
            break

        cont_pic += 1

        cv.imwrite(destination + "/figure" + str(cont_pic) + ".jpg", frame)
        print(f"# foto numero {cont_pic} tomada")

        sleep(0.5)
        if cont_pic == 30: break
    
    return pics 


def detect_corners(pics):
    cornerSize = (8,5) # TAMAÑO DEL TABLERO DE AJEDREZ DE CALIBRCION

    criteria = (
    cv.TERM_CRITERIA_EPS +
    cv.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)



    ## CREAMOS UNA MATRIZ DE PUNTOS QUE VAN A REPRESENTAR LOS PUNTODS DEL TABLERO DE AJEDREZ

    objectPoints = np.zeros((cornerSize[0]*cornerSize[1], 3), np.float32)

    objectPoints[:, :2] = np.mgrid[
    0:cornerSize[0],
    0:cornerSize[1]
    ].T.reshape(-1, 2)



    ## ARREGLOS PARA GUARDAR LOS PUNTOS DE LA IMAGEN Y LOS PUNTOS DEL MUNDO REAL 

    objectPointsArray = []
    imagePointsArray = []

    ## BUSCAR LAS ESQUINAS EN CADA UNA DE LAS IMAGENES  

    for img in pics:
        # APLICAR ESCALA DE GRISES
        imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        ret, corners = cv.findChessboardCorners(imgGray, cornerSize, None)

        if ret:
            objectPointsArray.append(objectPoints)

            corners2 = cv.cornerSubPix(
            imgGray,
            corners =corners,
            winSize = (11, 11),
            zeroZone = (-1, -1),
            criteria = criteria
            )
            imagePointsArray.append(corners2)

            #DIBUJAR EN LA IMAGEN LAS ESQUINAS DETECTADAS

            img = cv.drawChessboardCorners(img, cornerSize, corners2, ret)
            cv.imshow("img", img)
            cv.waitKey(500)
        else:
            print("No se encontraron esquinas en la imagen")



        

def main():
    result = take_pics()
    detect_corners(result)



if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()

