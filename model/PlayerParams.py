class PlayerParams:

    # In tournaments with odd player number

    def __init__(self, player, playerID):
        self.__player = player
        self.__points = 0
        self.__buchholz = 0
        self.__playerID = playerID
        self.__didPause = False

    def set_points(self, points):
        if points < 0:
            raise ValueError("Points value must not be negative")
        self.__points = points

    def set_buchholz(self, buchholz):
        if buchholz < 0:
            raise ValueError("Points value must not be negative")
        self.__buchholz = buchholz

    def get_points(self):
        return self.__points

    def get_buchholz(self):
        return self.__buchholz

    def get_player(self):
        return self.__player

    def get_playerID(self):
        return self.__playerID

    def set_didPause(self):
        self.__didPause = True

    def get_didPause(self):
        return self.__didPause
