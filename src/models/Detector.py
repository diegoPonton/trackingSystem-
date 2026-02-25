import cv2 as cv
import cv2.aruco as aruco
import numpy as np

from .Robot import Robot, RobotState

class Detector:

    """
        Class of Detector    
        
    """


    def __init__(self, camera, arena, dict_aruco = aruco.DICT_4X4_250):
        """Constructor of the class
        Args:
            camera (Camera): camera object to be used by the detector
            arena (Arena): arena object to be used by the detector
            dict_aruco (int): dictionary of aruco markers to be used by the detector


        """
        self.__camera = camera
        self.__robots = []
        self.__id_robots = []
        self.__arena = arena
        self.__dict_aruco = dict_aruco

        self.__detectorParams = aruco.DetectorParameters()
        self.__dictionary = aruco.getPredefinedDictionary(self.__dict_aruco)
        self.__detector = aruco.ArucoDetector(self.__dictionary, self.__detectorParams)
        print("Detector has been initialized")



    def detect(self):
        """Method for detect the robots in the arena BY FRAME, it returns a list of robots detected and 
        the frame with the robots detected
        Returns:
            list: list of robots detected in the arena
            frame: frame with the robots detected 

        """

        ret, frame = self.__camera.get_frame()
        if not ret:
            raise RuntimeError("Camera Error: Camera is not working properly")
        
        trail = np.zeros_like(frame)
        markerCorners, markerIds, _ = self.__detector.detectMarkers(frame)
        ids = np.array(markerIds).flatten()
        if markerIds is not None and markerIds.size > 0:

            """
                TO DO:
                - VERIFY IF THE ROBOT IS MOVING O WORKING AND UPDATE THE STATE OF THE ROBOT
                - UDPATE THE SOURCE TO ADMIT ORIENTATION OF THE ROBOT
            """

            for i, mid in enumerate(ids):
                # if the robot is not in the list of robots detected, add it to the list
                
                points = markerCorners[i][0]
                cx, cy = int(points.mean(axis=0)[0]), int(points.mean(axis=0)[1])
                if(mid not in self.__id_robots):
                    self.__id_robots.append(mid) 
                    self.__robots.append(Robot(mid, (cx, cy), (0,0,0), RobotState.MOVING)) #################

                else:
                    # Update existing robot's state if it exists
                    self.__robots[self.__id_robots.index(mid)].update_state((cx, cy), 0, RobotState.MOVING) #################

                cv.circle(frame, (cx, cy), 6, (0, 125, 255), -1)
        return self.__robots, frame #return the list of robots detected and updated
    
