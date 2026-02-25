


class Arena:
    """Class for represent the arena, it contains the information of the arena such as the size and the position of the arucos.
    """

    def __init__(self, size, arucos):
        """Constructor of the class, initialize the size and the arucos of the arena

        Args:
            size (tuple): size of the arena (width, height)
            arucos (list): list of arucos in the arena
        """
        self.__size = size
        self.__arucos = arucos

        