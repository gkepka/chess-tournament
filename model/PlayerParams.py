class PlayerParams:
    def __init__(self, player, tournament):
        self.player = player
        self.tournament = tournament
        self.__points = 0
        self.__buchholz = 0
        self.__did_pause = False
        self.eliminated = False

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

    def set_did_pause(self, did_pause):
        self.__did_pause = did_pause

    def get_did_pause(self):
        return self.__did_pause
