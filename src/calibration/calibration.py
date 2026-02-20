import cv2 as cv
import numpy as np



cap = cv.VideoCapture(0) #change if it is neccesary 

def take_pics():
    ret, frame = cap.read()
    return frame if ret else -1



def main():
    result = take_pics()

    while True:
        if result != -1:
            cv.imshow("camera", result)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()

