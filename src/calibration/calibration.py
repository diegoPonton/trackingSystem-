import cv2 as cv
import numpy as np
from time import sleep
import file

destination = "./../../tmp/figs/calibration/"

cap = cv.VideoCapture(0) #change if it is neccesary 

def take_pics(num_pics = 30):

    cont_pic = 0

    print("##### Tomando fotos para la calibracion")
    pics = []
    while cont_pic < num_pics:
        ret, frame = cap.read()  
        if ret: pics.append(frame) else break

        cont_pic += 1

        cv.imwrite(destination + "/figure" + str(cont_pic) + ".jpg", frame)
        print(f"# foto numero {cont_pic} tomada")

        sleep(1)
        if cont_pic == 30: break
    
    return pics 



def main():
    result = take_pics()

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()

