class PlayerParams:

    def __init__(self, player):
        self.__player = player
        self.__points = 0
        self.__buchholz = 0

    def set_points(self, points):
        if points < 0:
            raise ValueError("Points value must not be negative")
        self.__points = points

    def set_buchholz(self, buchholz):
        if buchholz < 0:
            raise ValueError("Points value must not be negative")
        self.__buchholz = buchholz
