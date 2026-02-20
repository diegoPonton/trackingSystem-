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



def main():
    result = take_pics()

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()

