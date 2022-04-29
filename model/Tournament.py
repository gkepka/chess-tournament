from model import *
from dao.DataAccessObjects import PlayerParamsDAO


class Tournament:

    # Constructor assumes number of rounds as parameter

    def __init__(self, max_players, max_rounds, tournament_id = None):
        self.__params_list = []
        self.__rounds_list = []
        self.max_players = max_players
        self.max_rounds = max_rounds
        self.tournament_id = tournament_id
        self.scores = [[-1] * max_rounds for _ in range(max_rounds)]

    def add_player_params_from_player(self, player):
        if not isinstance(player, Player):
            raise TypeError()
        player_params_dao = PlayerParamsDAO()
        player_params = player_params_dao.get_player_params_for_tournament(self)
        if len(player_params) == 0:
            self.__params_list.append(PlayerParams(player, self))
        else:
            player_params = [params for params in player_params if params.player.player_id == player.player_id]
            self.__params_list.extend(player_params)

    def add_player_params(self, player_params):
        self.__params_list.append(player_params)

    def next_round(self):
        next_round = Round(self, len(self.__rounds_list) + 1)
        self.__rounds_list += next_round

    # Function count_scores counts number of points of a player(playerID)
    def count_scores(self, playerID):
        sum = 0
        for i in range(len(self.__params_list)):
            if self.scores[i][playerID] != -1:
                sum += self.scores[i][playerID]
        return sum

    # Function count_Buholtz counts Buholtz of a player(playerID)

    def count_Buholtz(self, playerID):
        sum = 0
        for i in range(len(self.__params_list)):
            if self.scores[i][playerID] != -1:
                sum += self.count_scores(playerID)
        return sum

    # Sorts tuple by given element

    def Sort_Tuple(self, tup, elem):

        tup.sort(key=lambda x: x[elem], reverse=True)
        return tup

    # Function get_scores counts points and Buholtz of all the players than sorts the scores, returns current scores

    def get_scores(self):
        points = []
        for i in range(len(self.__params_list)):
            points.append((i, self.count_scores(i), self.count_Buholtz(i)))
        self.Sort_Tuple(points, 1)
        for i in range(len(self.__params_list) - 1):
            if points[i][1] == points[i + 1][1]:
                if self.count_Buholtz(i + 1) > self.count_Buholtz(i):
                    points[i], points[i + 1] = points[i + 1], points[i]
        for i in range(len(self.__params_list) - 1):
            if points[i][1] == points[i + 1]:
                if points[i][2] == points[i + 1][2]:
                    if self.scores[points[i][0]][points[i + 1][0]] == 0:
                        points[i], points[i + 1] = points[i + 1], points[i]
        return points

    # Function prints scores

    def print_scores(self):
        print(self.get_scores())

    # Function updates the scores

    def set_match_score(self, match):
        self.scores[match.player_white.playerID][match.player_black.playerID] = match.result
        if match.result == 0:
            self.scores[match.player_black.playerID][match.player_white.playerID] == 1
        if match.result == 1:
            self.scores[match.player_black.playerID][match.player_white.playerID] == 0
        if match.result == 0.5:
            self.scores[match.player_black.playerID][match.player_white.playerID] == 0.5
