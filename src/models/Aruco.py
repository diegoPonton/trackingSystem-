

class Aruco:
    """ 
    
    """


    def __init__(self, id, parent_id, marker_size = 250):
        """Constructor of the class, initialize the id, parent_id and position of the aruco
        Args:
            id (int): id of the aruco
            parent_id (int): id of the parent aruco (0 - robot; 1 - Arena)
            position (tuple): position of the aruco (x, y)
        """
        self.__id = id
        self.__parent_id = parent_id
        self.__marker_size = marker_size


    def get_id(self):
        """ Method for obtain the id of the aruco
        Returns:
            int: id of the aruco
        
        """
        return self.__id


    def get_parent_id(self):
        """ Method for obtain the parent id of the aruco
        Returns:
            int: parent id of the aruco
        
        """
        return self.__parent_id


    def get_marker_size(self):
        """ Method for obtain the marker size of the aruco
        Returns:
            int: marker size of the aruco
        
        """
        return self.__marker_size

        