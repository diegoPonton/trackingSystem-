

import cv2 as cv    

class System:
    """
       System of the tracking system, it is responsible for managing the different components of the system, 
       such as the detector, the aruco markers and the robots. 
       It also manages the state of the system and the communication between the different components.
    """

    def __init__(self, detector):
        self.__detector = detector





    def start(self):
        while True:
            robots, frame = self.__detector.detect()

            cv.imshow("Frame", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break




    def save_arucos():
        pass