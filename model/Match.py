class Match:

    # Result from white player perspective

    def __init__(self, tournament, round, player_white, player_black, result, match_id = None):
        self.tournament = tournament
        self.round = round
        self.player_white = player_white
        self.player_black = player_black
        self.result = result
        self.match_id = match_id

    def get_result(self):
        return self.result

    def set_result(self, result): # 1 - white wins, 0 - black wins, 0.5 - draw
        self.result = result
        if result == 1:
            self.eliminate_player(self.player_black, True)
            self.eliminate_player(self.player_white, False)
        if result == 0:
            self.eliminate_player(self.player_white, True)
            self.eliminate_player(self.player_black, False)
        if result == 0.5:
            self.eliminate_player(self.player_white, False)
            self.eliminate_player(self.player_black, False)

    def eliminate_player(self, player, value):
        player_params = [params for params in self.tournament.params_list if params.player == player]
        player_params[0].eliminated = value
