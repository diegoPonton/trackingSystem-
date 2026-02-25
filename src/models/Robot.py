
from enum import Enum
from .Aruco import Aruco

class RobotState(Enum):
    MOVING = 1,
    WAITING = 2,
    UNINITIALIZED = 3



class Robot(Aruco):
    """ Class for represent the robot, it has the id, position and orientation of the robot
    """
    
    def __init__(self, id, position, orientation, robot_state = RobotState.UNINITIALIZED):
        """Constructor of the class, initialize the id, position and orientation of the robot
        Args:
            id (int): id of the robot
            position (tuple): position of the robot (x, y)
            orientation (float): orientation of the robot in degrees
        """

        self.__position = position
        self.__orientation = orientation
        self.robot_state = robot_state

        super().__init__(id, 0) ## el parent_id del robot es 0


    def get_position(self):
        """ Method for obtain the position of the robot
        Returns:
            tuple: position of the robot (x, y)
        
        """
        return self.__position
    
    def get_orientation(self):
        """ Method for obtain the orientation of the robot
        Returns:
            float: orientation of the robot in degrees
        
        """
        return self.__orientation
    



    def update_state(self, position, orientation, robot_state):
        """ Method for update the state of the robot
        Args:
            position (tuple): position of the robot (x, y)
            orientation (float): orientation of the robot in degrees
            robot_state (RobotState): state of the robot

        """
        self.__position = position
        self.__orientation = orientation
        self.robot_state = robot_state