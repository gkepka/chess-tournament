from model import *


class Tournament:

    def __init__(self):
        self.__params_list = []
        self.__rounds_list = []

    def add_player(self, player):
        if not isinstance(player, Player):
            raise TypeError()
        player_params = PlayerParams(player)
        self.__params_list += player_params

    def next_round(self):
        next_round = Round(self, len(self.__rounds_list) + 1)
        self.__rounds_list += next_round
